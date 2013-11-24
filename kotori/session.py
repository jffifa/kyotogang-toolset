#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import cookielib
import urllib
import urllib2
import parser
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

    def login(self):
        postData = {
            'fastloginfield':'username',
            'username':self.username,
            'password':self.password,
            'quickforward':'yes',
            'handlekey':'ls',
        }
        encPostData = urllib.urlencode(postData)
        res = self.stream.open(self.loginUrl, encPostData)

        if parser.verifyLogin(res.read()):
            self.status = gconf.SESSION_STATUS_LOGIN
        else:
            self.status = gconf.SESSION_STATUS_LOGOUT

        if gconf.DEBUG:
            print res.read()
    
    def keep_connect(self):
        if gconf.DEBUG:
            print self.username, self.status

        if self.status == gconf.SESSION_STATUS_LOGIN:
            res = self.stream.open(self.keepConnUrl)

        """"
        if gconf.DEBUG:
            for item in self.cookie:
                print item.name, item.value
            print res.read()
        """

    def logout(self):
        pass
