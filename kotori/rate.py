#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import session
import xmlparser
import time
import random
import urlparse
import urllib
import urllib2
import copy
from gconf import GConf as gconf

class Rate(object):
    def __init__(self):
        pass

    def gen_timestamp(self):
        return str(int(time.time()))+str(random.randint(100, 999))

    def get_rate_form(self, tid, pid, session):
        queryDict = copy.copy(gconf.RATE_FORM_QUERY_DICT)
        timestamp = self.gen_timestamp()
        queryDict['t'] = timestamp
        queryDict['tid'] = str(tid)
        queryDict['pid'] = str(pid)
        rateFormUrl = urlparse.urlunparse((
            gconf.PROTOCOL,
            gconf.BASE_URL,
            gconf.RATE_FORM_PATH,
            '',
            urllib.urlencode(queryDict),
            ''))

        rateFormHeader = copy.copy(gconf.RATE_FORM_HEADER)
        rateFormRef = urlparse.urlunparse((
            gconf.PROTOCOL,
            gconf.BASE_URL,
            gconf.FORUM_PATH,
            '',
            urllib.urlencode({
                'mod':'viewthread',
                'tid':str(tid),
                }),
            ''))
        rateFormHeader['Referer'] = rateFormRef

        req = urllib2.Request(url=rateFormUrl, headers=rateFormHeader)
        cookie = session.get_cookie() # ensure its thread safety
        cookie.add_cookie_header(req)
        
        res = urllib2.urlopen(req)

        return res.read()

    def get_rate_limit(self, session):
        rateFormStr = self.get_rate_form(tid=gconf.RATE_LIM_TID, pid=gconf.RATE_LIM_PID, session=session)
        rateLimit = xmlparser.parse_rate_limit(rateFormStr)
        if rateLimit is None or rateLimit < 0:
            rateLimit = 0
        return rateLimit

    def get_page(floor):
        return (floor-1)/gconf.POST_PER_PAGE+1

    def get_pid_author(session, tid, floor):
        pass

    def rate(self, session, c, tid, floor):
        if self.get_rate_limit(session) < 0:
            return False
        if c > gconf.MAX_RATE_CONCURRENCY:
            c = gconf.MAX_RATE_CONCURRENCY

        page = self.get_page(floor)
        pid, author = self.get_pid_author(tid, floor)

        rateHeader = copy.copy(gconf.RATE_HEADER)
        rateRef = urlparse.urlunparse((
            gconf.PROTOCOL,
            gconf.BASE_URL,
            gconf.FORUM_PATH,
            '',
            urllib.urlencode({
                'mod':'viewthread',
                'tid':str(tid),
                'page':str(page)
                }),
            ''))
        rateHeader['Referer'] = rateRef

    def multi_rate(self):
        pass

if __name__ == '__main__':
    s = session.Session(username='jffifa', password='123456')
    s.login()
    time.sleep(1)
    s.keep_connect()
    r = Rate()
    print r.get_rate_limit(session=s)
