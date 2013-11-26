#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser
import re
from gconf import GConf as gconf

def test(x):
    print x

def parseXML(xmlStr):
    return ET.fromstring(xmlStr).text

def verify_login(loginResStr):
    s = parseXML(loginResStr)
    if s.find(gconf.FORUM_URL) == -1:
        return False
    else:
        return True

def parse_rate_limit(rateFormStr):
    class RateLimParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.tdCnt = 0
            self.rateLim = None
        def handle_starttag(self, tag, attrs):
            if tag == 'td':
                self.tdCnt += 1
        
        def handle_data(self, data):
            if self.rateLim is None and self.tdCnt == 4: # magic number
                self.rateLim = int(data)
    s = parseXML(rateFormStr)
    p = RateLimParser()
    p.feed(s)
    return p.rateLim

def parse_pid_user(htmlStr, pageFloor):
    """parse pid and author"""
    class PidUserParser(HTMLParser):
        def __init__(self, floor):
            HTMLParser.__init__(self)
            self.postCnt = 0
            self.floor = floor
            self.authi = False
            self.author = False
            self.pidRe = re.compile(r'post_(\d+)')
            self.authorRe = re.compile(r'space-uid-\d+')
            self.info = {
                    'pid':0,
                    'author':'',
                    }
        def handle_starttag(self, tag, attrs):
            if tag == 'div':
                attrDict = dict(attrs)
                if 'id' in attrDict:
                    mObj = self.pidRe.match(attrDict['id'])
                    if mObj:
                        self.postCnt += 1
                        if self.postCnt == self.floor:
                            self.info['pid'] = mObj.group(1)
                elif attrDict.get('class') == 'authi' and self.postCnt == self.floor:
                    self.authi = True
                else:
                    self.authi = False
            elif tag == 'a' and self.authi:
                attrDict = dict(attrs)
                mObj = self.authorRe.match(attrDict['href'])
                if mObj:
                    self.author = True
        def handle_data(self, data):
            if self.author:
                self.info['author'] = data
                self.authi = False
                self.author = False

    p = PidUserParser(pageFloor)
    p.feed(htmlStr)
    return p.info


# test case
if __name__ == '__main__':
    pass
