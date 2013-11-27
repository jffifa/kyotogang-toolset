#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser
import re
from gconf import GConf as gconf

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
                try:
                    self.rateLim = int(data)
                except Exception as e:
                    self.rateLim = -65536
                    pass
    s = parseXML(rateFormStr)
    p = RateLimParser()
    p.feed(s)
    return p.rateLim

def parse_pid_author(htmlStr, pageFloor):
    """parse pid and author"""
    class PidAuthorParser(HTMLParser):
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
                            try:
                                self.info['pid'] = int(mObj.group(1))
                            except:
                                pass
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

    p = PidAuthorParser(pageFloor)
    p.feed(htmlStr)
    return (p.info['pid'], p.info['author'])

def parse_rate_form(xmlStr):
    class RateFormParser(HTMLParser): # maybe integrate with RateLimParser?
        def __init__(self):
            HTMLParser.__init__(self)
            self.table = {
                    'formhash':'',
                    'tid':'',
                    'pid':'',
                    'referer':'',
                    'handlekey':'',
                    }

        def handle_startendtag(self, tag, attrs):
            if tag == 'input':
                attr_dict = dict(attrs)
                if attr_dict['name'] in self.table:
                    self.table[attr_dict['name']] = attr_dict['value']

        def handle_starttag(self, tag, attrs):
            if tag == 'input':
                attr_dict = dict(attrs)
                if attr_dict['name'] in self.table:
                    self.table[attr_dict['name']] = attr_dict['value']

    root = ET.fromstring(xmlStr)
    htmlStr = root.text
    p = RateFormParser()
    p.feed(htmlStr)
    return p.table

# test case
if __name__ == '__main__':
    pass
