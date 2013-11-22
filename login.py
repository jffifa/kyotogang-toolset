#!/usr/bin/env python2
import urllib
import urllib2
import cookielib
import time

LOGIN_URL = 'http://bbs.saraba1st.com/2b/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
LOGIN_REFERER = 'http://bbs.saraba1st.com/2b/forum-6-1.html'

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
        'username':'algorithms',
        'password':'kye021li',
        'quickforward':'yes',
        'handlekey':'ls',
        }

ret = opener.open(LOGIN_URL, urllib.urlencode(data))
response_header = ret.info()
print response_header.items()
for item in cookie:
    print item.name, item.value
print ret.read()
#"""
for i in xrange(5):
    print '.'
    time.sleep(1)
#"""
ret = opener.open(LOGIN_REFERER)
for item in cookie:
    print item.name, item.value
print ret.read()

