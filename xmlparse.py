#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser
import re
#tree = ET.parse('xml')
#root = tree.getroot()
#print root.tag, root.attrib, root.text

def test():
    print 'hello world'

class myHtmlParser(HTMLParser):
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

def getForm(xmlStr):
    root = ET.fromstring(xmlStr)
    htmlStr = root.text
    #print htmlStr
    htmlParser = myHtmlParser()
    htmlParser.feed(htmlStr)
    return htmlParser.table

class getPidParser(HTMLParser):
    def __init__(self, floor):
        HTMLParser.__init__(self)
        self.postCnt = 0
        self.floor = floor
        self.authi = False
        self.author = False
        self.re = re.compile(r'post_(\d+)')
        self.info = {
                'pid':'',
                'author':'',
                }

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            attr_dict = dict(attrs)
            if 'id' in attr_dict:
                mObj = self.re.match(attr_dict['id'])
                if mObj:
                    self.postCnt += 1
                    if self.postCnt == self.floor:
                        self.info['pid'] = mObj.group(1)
            elif attr_dict.get('class') == 'authi' and self.postCnt == self.floor:
                self.authi = True
            else:
                self.authi = False
        elif tag == 'a' and self.authi:
            attr_dict = dict(attrs)
            mObj = re.compile(r'space-uid-\d+').match(attr_dict['href'])
            if mObj:
                self.author = True

    def handle_data(self, data):
        if self.author:
            self.info['author'] = data
            self.authi = False
            self.author = False

def getPid(htmlStr, floor):
    htmlParser = getPidParser(floor)
    htmlParser.feed(htmlStr)
    return htmlParser.info

