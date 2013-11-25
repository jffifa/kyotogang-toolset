#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import session
import time
import threading
import Queue
from gconf import GConf as gconf

class LoginThread(threading.Thread):
    """login thread
    """

    def __init__(self, interval, userQueue, sessions):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interval = interval
        self.intCnt = 0
        self.threadStop = False
        self.sessions = sessions
        # userQueue is a tuple where the firse element is username and the second password
        self.userQueue = userQueue 

        for u in self.sessions.itervalues():
            self.userQueue.put(u.username)

    def run(self):
        # login each session
        for session in self.sessions.itervalues():
            session.login()
            self.userQueue.get()
            self.userQueue.task_done()
        
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
        #self.users = {}
        self.sessions = {}
        self.loginThread = None
        self.logined = False

    def add_user(self, username='', password=''):
        self.sessions[username] = session.Session(
            username = username,
            password = password)
    
    def clear_users(self):
        self.sessions = {}

    def login(self):
        q = Queue.Queue(gconf.MAX_USER)
        self.loginThread = LoginThread(
            interval = self.__class__.THREAD_INTERVAL,
            userQueue = q,
            sessions = self.sessions)
        self.loginThread.start()
        q.join()
        self.logined = True

        if gconf.DEBUG:
            for u in self.sessions.itervalues():
                print u.username, u.status

    def logout(self):
        self.loginThread.stop()
        self.loginThread.join()
        self.loginThread = None
        self.clear_users()
        self.logined = False

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
    lc.add_user('jffifa', '123456')
    #lc.add_user('狂三小天使', '134134')
    lc.login()
    time.sleep(5)
    lc.logout()

