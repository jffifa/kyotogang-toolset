#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import session
import time
import threading
from gconf import GConf as gconf

class LoginThread(threading.Thread):
    """login thread
    """

    def __init__(self, interval=30):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interval = interval
        self.intCnt = 0
        self.sessions = {}
        self.threadStop = False

    def get_status(self):
        return dict([(u, s.status) for (u, s) in self.sessions.iteritems()])

    def run(self):
        # login each session
        for session in self.sessions.itervalues():
            session.login()
        
        # loop for sessions to keep connect
        while not self.threadStop:
            time.sleep(1)
            self.intCnt += 1
            if self.intCnt == self.interval:
                self.intCnt = 0
                for session in self.sessions.itervalues():
                    session.keep_connect()

        # stop and logout
        for session in self.sessions.itervalues():
            session.logout()
        self.sessions.clear()

    def stop(self):
        self.threadStop = True


class LoginCtrl(object):
    """login controller
    """


    THREAD_INTERVAL = 30 # keep connect every THREAD_INTERVAL seconds


    def __init__(self):
        self.users = {}
        self.loginThread = None

    def add_user(self, username='', password=''):
        self.users[username] = {
            'username':username, 
            'password':password,
            'status':gconf.SESSION_STATUS_INIT
            }


    def login(self):
        self.loginThread = LoginThread(self.__class__.THREAD_INTERVAL)
        for user in self.users.itervalues():
            self.loginThread.sessions[user['username']] = session.Session(
                username=user['username'],
                password=user['password'])
        self.loginThread.start()
        while True:
            statuses = self.loginThread.get_status()
            if gconf.SESSION_STATUS_INIT in statuses.itervalues():
                time.sleep(1)
            else:
                for username, status in statuses.iteritems():
                    self.users[username]['status'] = status
                break

    def logout(self):
        self.loginThread.stop()
        self.loginThread.join()
        self.loginThread = None

    def relogin(self):
        if self.loginThread:
            self.logout()
            self.login()
        else:
            self.login()

# test case
if __name__ == '__main__':
    lc = LoginCtrl()
    lc.add_user('内田彩', '134134')
    lc.add_user('狂三小天使', '134134')
    lc.login()
    print lc.users['内田彩']['status']
    print lc.users['狂三小天使']['status']
    lc.logout()

