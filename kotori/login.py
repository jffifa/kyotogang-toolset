#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import session
import time
import threading

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

    def add_user(self, username='', password='', enable=True):
        self.users[username] = {
            'username':username, 
            'password':password,
            'enable':enable,
            }

    def set_enable(self, username='', enable=True):
        if username in self.users:
            self.users[username]['enable'] = enable

    def login(self):
        self.loginThread = LoginThread(self.__class__.THREAD_INTERVAL)
        for user in self.users.itervalues():
            if (user['enable']):
                self.loginThread.sessions[user['username']] = session.Session(
                    username=user['username'],
                    password=user['password'])
        self.loginThread.start()

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

