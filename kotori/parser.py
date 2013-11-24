#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET
import HTMLParser
import re
from gconf import GConf as gconf

def parseXML(xmlStr):
    return ET.fromstring(xmlStr).text

def verifyLogin(loginResStr):
    s = parseXML(loginResStr)
    if s.find(gconf.FORUM_URL) == -1:
        return False
    else:
        return True
