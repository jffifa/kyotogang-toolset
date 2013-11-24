#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
from kotori import *
from kotori.gconf import GConf as gconf
import sys
import codecs
import getpass
import time

def s(u_str):
    return u_str.encode(gconf.SHELL_ENCODING)

def t(str):
    return str.decode(gconf.SHELL_ENCODING)

def p_kotori():
    pass

def p_cutline():
    print
    print '================================'

def p_usage():
    p_cutline()
    usg = u"""命令列表(按下命令后按回车，跟着提示走^_^):
    a: 添加用户
    d: 删除用户
    l: 开始登录挂机
    r: 重新登录(如果开始挂机后添加用户，需要重新登录才能生效)
    p: 显示当前已经添加的用户列表
    q: 退出"""
    print s(usg)

def p_user_data(userData=[]):
    p_cutline()
    print s(u'当前已添加的用户列表:')
    if len(userData) == 0:
        print s(u'无')
    else:
        for u in enumerate(userData, start=1):
            print str(u[0])+'>', u[1][0]

def add_user(userData=[]):
    p_cutline()
    username = raw_input(s(u'请输入用户名: '))
    password = ''
    while True:
        print s(u'请输入密码(屏幕上不会显示):'),
        pwd1 = getpass.getpass('')
        print s(u'请再次输入密码:'),
        pwd2 = getpass.getpass('')
        if pwd1 != pwd2:
            print s(u'两次输入密码不一致！')
        else:
            password = pwd1
            break
    userData.append((t(username).encode(gconf.INTERNAL_ENCODING), password))
    userdata.UserData().save_user_data(userData)

def del_user(userData=[]):
    p_user_data(userData)
    username = raw_input(s(u'请输入用户编号或用户名(0表示清空): '))
    uid = -1
    try:
        uid = int(username)
    except:
        pass
    if uid == -1:
        pass
    elif uid == 0:
        pass
    else:
        pass

def login(userData=[]):
    pass

def relogin(userData=[]):
    pass

if __name__ == '__main__':
    try:
        group_id = raw_input(s(u'请输入群号: '))

        if group_id != gconf.GROUP_ID:
            print s(u'抱歉！该工具仅限内部使用！')
            import time
            time.sleep(1)
            sys.exit(0)

        p_kotori()
        userData = userdata.UserData().load_user_data()
        p_user_data(userData)

        while True:
            p_usage()
            cmd = raw_input(s(u'请输入命令: '))
            if cmd == 'a':
                add_user(userData)
            elif cmd == 'd':
                del_user(userData)
            elif cmd == 'p':
                p_user_data(userData)
            elif cmd == 'q':
                break
        
    except KeyboardInterrupt:
        sys.exit(1)
