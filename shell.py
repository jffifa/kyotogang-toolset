#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
from kotori import *
import sys

if __name__ == '__main__':
    try:
        loginCtrl = login.LoginCtrl()
        loginCtrl.add_user('内田彩', '134134')
        loginCtrl.login()
        s = raw_input('....')
    except KeyboardInterrupt:
        loginCtrl.logout()
        sys.exit(1)
