#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import os
import urlparse
import urllib

class GConf:
    """global configuration
    """


    # debug mode
    DEBUG = True

    # global dir settings
    BASE_DIR = os.path.dirname(__file__)

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

    # fake user agent
    FAKE_UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML: like Gecko) Chrome/31.0.1650.57 Safari/537.36'

    # http header
    LOGIN_HEADER = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'User-Agent':FAKE_UA,
        'Origin':ORIGIN_URL,
        'Referer':FORUM_URL ,
        }

