#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import sys
import os
import urlparse
import urllib

class GConf:
    """global configuration
    """

    GROUP_ID = '10079277'
    
    # encodings
    SHELL_ENCODING = sys.stdout.encoding
    INTERNAL_ENCODING = 'utf_8'

    # debug mode
    DEBUG = False

    # global dir and file path settings
    BASE_DIR = os.path.dirname(__file__)
    USER_DATA_PATH = os.path.join(BASE_DIR, 'data', 'user')

    # global conf for urls
    PROTOCOL = 'http'
    BASE_URL = 'bbs.saraba1st.com'

    # http origin url
    ORIGIN_URL = urlparse.urlunparse((PROTOCOL, BASE_URL, '', '', '', ''))

    # forum homepage url
    FORUM_PATH = '/2b/forum.php'
    FORUM_URL = urlparse.urlunparse((PROTOCOL, BASE_URL, FORUM_PATH, '', '', ''))

    # ajax login url
    LOGIN_PATH = '/2b/member.php'
    LOGIN_QUERY = urllib.urlencode({
        'mod':'logging',
        'action':'login',
        'loginsubmit':'yes',
        'infloat':'yes',
        'lssubmit':'yes',
        'inajax':'1',
        })
    LOGIN_URL = urlparse.urlunparse((PROTOCOL, BASE_URL, LOGIN_PATH, '', LOGIN_QUERY, ''))

    # session keeping url
    KEEP_CONN_PATH = '/2b/home.php'
    KEEP_CONN_QUERY = urllib.urlencode({
        'mod':'spacecp',
        'ac':'credit',
        'showcredit':'1'
        })
    KEEP_CONN_URL = urlparse.urlunparse((PROTOCOL, BASE_URL, KEEP_CONN_PATH, '', KEEP_CONN_QUERY, ''))

    # get rate form url
    RATE_LIM_TID = 643316
    RATE_LIM_PID = 22412315
    RATE_FORM_PATH = '/2b/forum.php'
    RATE_FORM_QUERY_DICT = {
        'mod':'misc',
        'action':'rate',
        #'t':'1385395649378',
        #'tid':'643316',
        #'pid':'22412315',
        'infloat':'yes',
        'handlekey':'rate',
        'inajax':'1',
        'ajaxtarget':'fwin_content_rate',
        }

    RATE_PATH = FORUM_PATH
    RATE_QUERY = urllib.urlencode({
        'mod':'misc',
        'action':'rate',
        'ratesubmit':'yes',
        'infloat':'yes',
        'inajax':'1'
        })
    RATE_URL = urlparse.urlunparse((
        PROTOCOL, 
        BASE_URL,
        FORUM_PATH,
        '',
        RATE_QUERY,
        ''))

    # fake user agent
    FAKE_UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML: like Gecko) Chrome/31.0.1650.57 Safari/537.36'

    # http header
    LOGIN_HEADER = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6',
        'Cache-Control':'max-age=0',
        #'Connection':'keep-alive',
        'Connection':'close',
        'User-Agent':FAKE_UA,
        'Origin':ORIGIN_URL,
        'Referer':FORUM_URL ,
        }

    RATE_FORM_HEADER = {
        'Accept':'*/*',
        'Accept-Language':'zh-CN,zh;q=0.8:ja;q=0.6',
        #'Connection':'keep-alive',
        'Connection':'close',
        'User-Agent':FAKE_UA,
        #'Referer':'http://bbs.saraba1st.com/2b/forum.php?mod=viewthread&tid=643316',
        'X-Requested-With':'XMLHttpRequest',
        }

    RATE_HEADER = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp:*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8:ja;q=0.6',
        'Cache-Control':'max-age=0',
        #'Connection':'keep-alive',
        'Connection':'close',
        'User-Agent':FAKE_UA,
        'Origin':ORIGIN_URL,
        #'Referer':'http://bbs.saraba1st.com/2b/forum.php?mod=viewthread&tid=974473&page=1',
        }

    # session status
    SESSION_STATUS_INIT = 0
    SESSION_STATUS_LOGIN = 1
    SESSION_STATUS_LOGOUT = 2
    SESSION_STATUS_CONN = 3

    # max users
    MAX_USER = 256

    POST_PER_PAGE = 30

    MAX_RATE_CONCURRENCY = 768
