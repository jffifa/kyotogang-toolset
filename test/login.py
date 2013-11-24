#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import urllib
import urllib2
import cookielib
import time
import threading
import copy
import xmlparse

LOGIN_URL = 'http://bbs.saraba1st.com/2b/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
LOGIN_REFERER = 'http://bbs.saraba1st.com/2b/forum-6-1.html'
LOGIN_TEST = 'http://bbs.saraba1st.com/2b/home.php?mod=spacecp&ac=credit&showcredit=1'
RATE_REFERER = 'http://bbs.saraba1st.com/2b/forum.php?mod=viewthread&tid=974473&page=1'
USERNAME = '内田彩'
PASSWORD = '134134'

cookie = cookielib.CookieJar()
login_header = [
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
        #('Accept-Encoding','gzip,deflate,sdch'),
        ('Accept-Language','zh-CN,zh;q=0.8,ja;q=0.6'),
        ('Cache-Control','max-age=0'),
        ('Connection','keep-alive'),
        ('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'),
        ('Origin','http://bbs.saraba1st.com'),
        ('Referer','http://bbs.saraba1st.com/2b/forum.php'),
        ]
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
opener.addheaders = login_header
data = {
        'fastloginfield':'username',
        'username':USERNAME,
        'password':PASSWORD,
        'quickforward':'yes',
        'handlekey':'ls',
        }

ret = opener.open(LOGIN_URL, urllib.urlencode(data))
print ret.read()

loginRetSession = copy.copy(ret)
"""
response_header = ret.info()
print response_header.items()
for item in cookie:
    print item.name, item.value
print ret.read()
for i in xrange(5):
    print '.'
    time.sleep(1)
ret = opener.open(LOGIN_TEST)
for item in cookie:
    print item.name, item.value
print ret.read()
"""

#here we need to get pid
POST_PER_PAGE = 30
TID = 974473
FLOOR = 32
page = (FLOOR-1)/POST_PER_PAGE+1
#print page
GET_PID_URL = '-'.join(['http://bbs.saraba1st.com/2b/thread',str(TID),str(page),'1'])+'.html'
tmp = opener.open(GET_PID_URL)
getPidStr = tmp.read()
print xmlparse.getPid(getPidStr, FLOOR-POST_PER_PAGE*(page-1))

#now we have logined
RATE_PRE_URL='http://bbs.saraba1st.com/2b/forum.php?mod=misc&action=rate&tid=974473&pid=23656423&infloat=yes&handlekey=rate&t=1385210550256&inajax=1&ajaxtarget=fwin_content_rate' # here param t is timestamp
rate_pre_header = [
        ('Accept', '*/*'),
        #('Accept-Encoding','gzip,deflate,sdch'),
        ('Accept-Language','zh-CN,zh;q=0.8,ja;q=0.6'),
        #('Cache-Control','max-age=0'),
        ('Connection','keep-alive'),
        ('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'),
        #('Origin','http://bbs.saraba1st.com'),
        ('Referer','http://bbs.saraba1st.com/2b/forum.php?mod=viewthread&tid=974473&page=1'),
        ('X-Requested-With','XMLHttpRequest'),
        ]
opener.addheaders = rate_pre_header
ret = opener.open(RATE_PRE_URL)
formStr = ret.read()
#print formStr

table = xmlparse.getForm(formStr)

#now we got the rate form
print table

RATE_URL='http://bbs.saraba1st.com/2b/forum.php?mod=misc&action=rate&ratesubmit=yes&infloat=yes&inajax=1'
rate_header = [
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
        #('Accept-Encoding','gzip,deflate,sdch'),
        ('Accept-Language','zh-CN,zh;q=0.8,ja;q=0.6'),
        ('Cache-Control','max-age=0'),
        ('Connection','keep-alive'),
        ('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'),
        ('Origin','http://bbs.saraba1st.com'),
        ('Referer','http://bbs.saraba1st.com/2b/forum.php?mod=viewthread&tid=974473&page=1'),
        ]
rate_header = dict(rate_header)
rateData = table
rateData['score1'] = '1'
rateData['reason'] = '回血'
rateData['ratesubmit'] = 'true'
rateDataStr = urllib.urlencode(rateData)

RATE_CONCURRENCY = 1000
def doRate(req):
    ret = urllib2.urlopen(req)
    #print ret.read()
req = urllib2.Request(RATE_URL, rateDataStr, rate_header)
reqCookie = cookielib.CookieJar()
reqCookie.extract_cookies(loginRetSession, req)
reqCookie.extract_cookies(ret, req)
reqCookie.add_cookie_header(req)

"""
for i in xrange(RATE_CONCURRENCY):
    t = threading.Thread(target=doRate, args=(req,))
    t.start()
"""
"""
ret = opener.open(RATE_URL, urllib.urlencode(rateData))
print ret.read()
"""
