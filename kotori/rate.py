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
import threading
from gconf import GConf as gconf

class Rate(object):
    def __init__(self):
        pass

    def gen_timestamp(self):
        return str(int(time.time()))+str(random.randint(100, 999))

    def get_rate_form(self, session, tid, pid):
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
        if gconf.DEBUG:
            print rateFormUrl

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
        rateFormStr = self.get_rate_form(session=session, tid=gconf.RATE_LIM_TID, pid=gconf.RATE_LIM_PID)
        rateLimit = xmlparser.parse_rate_limit(rateFormStr)
        if rateLimit < 0:
            rateLimit = 0
        return rateLimit

    def get_page(self, floor):
        return (floor-1)/gconf.POST_PER_PAGE+1

    def get_pid_author(self, tid, floor):
        page = self.get_page(floor)
        url = urlparse.urlunparse((
            gconf.PROTOCOL,
            gconf.BASE_URL,
            '-'.join([
                '/2b/thread', # magic string hack ?
                str(tid),
                str(page),
                '1'])+'.html',
            '',
            '',
            ''))
        tmpSession = session.Session(username=None, password=None)
        htmlStr = tmpSession.open(url)
        #print htmlStr
        pid, author = xmlparser.parse_pid_author(htmlStr, floor-gconf.POST_PER_PAGE*(page-1))
        return (pid, author)

    def get_formtable(self, session, tid, pid):
        rateFormStr = self.get_rate_form(session=session, tid=tid, pid=pid)
        if gconf.DEBUG:
            print rateFormStr
        table = xmlparser.parse_rate_form(rateFormStr)
        # check tid and pid
        try:
            table['tid'] = int(table['tid'])
            table['pid'] = int(table['pid'])
            if tid==table['tid'] and pid==table['pid']:
                return table
            else:
                return None
        except:
            return None

    # rate thread
    def _doRate(self, req):
        """
        try:
            res = urllib2.urlopen(req)
            if gconf.DEBUG:
                print res
        except Exception as e:
            if gconf.DEBUG:
                print e
        """
        res = urllib2.urlopen(req)

    # rate reason should be a bytestring encoded in utf8
    def rate(self, session, rateSgn, rateReason, c, tid, pid, page, formtable):
        if c > gconf.MAX_RATE_CONCURRENCY:
            c = gconf.MAX_RATE_CONCURRENCY

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
        rateData = copy.copy(formtable)
        rateData['score1'] = str(rateSgn)
        rateData['reason'] = rateReason
        rateData['ratesubmit'] = 'true'
        if gconf.DEBUG:
            print rateData
        rateDataStr = urllib.urlencode(rateData)

        req = urllib2.Request(gconf.RATE_URL, rateDataStr, rateHeader)
        reqCookie = session.cookie
        reqCookie.add_cookie_header(req)

        threadList = []
        for i in xrange(c):
            threadList.append(threading.Thread(target=self._doRate, args=(req,)))
        for t in threadList:
            t.start()
        for t in threadList:
            t.join()

        return True

    def multi_rate(self, sessions, rateSgn, rateReasons, c, tid, pid, page):
        formtables = []
        for s in sessions:
            formtable = self.get_formtable(s, tid, pid)
            if formtable is None:
                return False
            else:
                formtables.append(formtable)

        rrateReasons = rateReasons[::-1]

        reslist = map(lambda s,rr,ft: self.rate(
            session=s,
            rateSgn=rateSgn,
            rateReason=rr,
            c=c,
            tid=tid,
            pid=pid,
            page=page,
            formtable=ft), sessions, rrateReasons, formtables);

        return reduce(lambda x,y:x and y, reslist)

if __name__ == '__main__':
    """
    s = session.Session(username='内田彩', password='134134')
    s.login()
    time.sleep(1)
    s.keep_connect()
    r = Rate()
    #print r.get_rate_limit(session=s)
    tid = 976137
    pid, author = r.get_pid_author(session=s, tid=tid, floor=51)
    #print (pid, author)
    formtable = r.get_formtable(session=s, tid=tid, pid=pid)
    #print formtable
    r.rate(session=s, rateSgn=-1, rateReason='沉了船我们还是朋友', c=2048, tid=tid, pid=pid, page=2, formtable=formtable)
    """
    r = Rate()
    tid = 976137
    s2 = session.Session(username=None, password=None)
    pid, author = r.get_pid_author(session=s2, tid=tid, floor=51)
    print pid, author
