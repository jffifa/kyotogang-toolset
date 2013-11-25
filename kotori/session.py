#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import cookielib
import urllib
import urllib2
import xmlparser
import time
from gconf import GConf as gconf

class Session(object):
    """stage1st session
    """


    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.loginUrl = gconf.LOGIN_URL
        self.keepConnUrl = gconf.KEEP_CONN_URL
        self.httpHeader = gconf.LOGIN_HEADER

        self.cookie = cookielib.CookieJar()
        self.stream = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.stream.addheaders = self.httpHeader.items()

        self.status = gconf.SESSION_STATUS_INIT
        self.lastRes = None # last time connect response

        self.mutex = False

    def get_cookie(self):
        return self.cookie # cookielib is thread safe itself

    # thread safe urlopen?
    def open(self, url, data=None):
        while self.mutex:
            sleep(0.1)
        self.mutex = True
        res = self.stream.open(url)
        s = res.read()
        self.mutex = False
        return s

    def login(self):
        postData = {
            'fastloginfield':'username',
            'username':self.username,
            'password':self.password,
            'quickforward':'yes',
            'handlekey':'ls',
        }
        encPostData = urllib.urlencode(postData)

        while self.mutex:
            sleep(0.1)
        self.mutex = True
        try:
            self.lastRes = self.stream.open(self.loginUrl, encPostData)
            resStr = self.lastRes.read()
        except urllib2.URLError as e:
            if gconf.DEBUG:
                print e.reason

        if (self.lastRes is not None) and (xmlparser.verify_login(resStr)):
            self.status = gconf.SESSION_STATUS_LOGIN
        else:
            self.status = gconf.SESSION_STATUS_LOGOUT
        self.mutex = False

        if gconf.DEBUG:
            print resStr
    
    def keep_connect(self):
        if gconf.DEBUG:
            print self.username, self.status

        while self.mutex:
            sleep(0.1)
        self.mutex = True
        try:
            if self.status == gconf.SESSION_STATUS_LOGIN:
                self.lastRes = self.stream.open(self.keepConnUrl)
        except urllib2.URLError as e:
            #self.status = gconf.SESSION_STATUS_LOGOUT
            if gconf.DEBUG:
                print e.reason
        self.mutex = False

        if gconf.DEBUG:
            for item in self.cookie:
                print item.name, item.value
            print self.lastRes.read()

    def logout(self):
        pass

# test case
if __name__ == '__main__':
    s = Session('jffifa', '123456')
    s.login()
    import time
    time.sleep(5)
    s.keep_connect()
