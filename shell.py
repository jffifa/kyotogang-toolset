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

def gnu(uname, passwd):
    return {
        'username':uname,
        'password':passwd,
        'status':gconf.SESSION_STATUS_INIT,
        'ratelim':-1,
        }

def lud():
    ud = userdata.UserData().load_user_data()
    return {u[0]: gnu(u[0], u[1]) for u in ud}

def sud(userData={}):
    l = [(u['username'], u['password']) for u in userData.values()]
    userdata.UserData().save_user_data(l)

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

def p_user_data(userData={}, showRatelim=False):
    p_cutline()
    print s(u'当前已添加的用户列表:')
    if len(userData) == 0:
        print s(u'无')
    else:
        for u in enumerate(userData.itervalues(), start=1):
            print str(u[0])+'>', s(u[1]['username'].decode(gconf.INTERNAL_ENCODING)),
            if u[1]['status'] == gconf.SESSION_STATUS_LOGIN:
                print s(u'[已登录]'),
            else:
                print s(u'[未登录]'),
            print

def add_user(userData=[]):
    p_cutline()
    username = t(raw_input(s(u'请输入用户名: '))).encode(gconf.INTERNAL_ENCODING)
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
    if username in userData:
        while True:
            c = raw_input(s(u'用户已存在, 是否覆盖(y=是, n=否): '))
            if c == 'y':
                userData[username]['password'] = password
                break
            elif c == 'n':
                confirm = False
                break
    else:
        userData[username] = gnu(username, password)

    sud(userData)

    if gconf.DEBUG:
        print userData

    return userData

def del_user(userData={}):
    while True:
        p_user_data(userData)
        username = t(raw_input(s(u'请输入用户编号或用户名(0表示清空, 直接回车取消): '))).encode(gconf.INTERNAL_ENCODING)
        uid = -1

        try:
            uid = int(username)
        except:
            pass

        if username == '':
            break
        elif uid == 0:
            userData = {}
            break
        else:
            if uid != -1:
                if uid < 0 or uid > len(userData):
                    print s(u'用户不存在')
                else:
                    un = userData.values()[uid-1]['username']
                    del userData[un]
                    break
            else:
                if not username in userData:
                    print s(u'用户不存在')
                else:
                    del userData[username]
                    break

    sud(userData)

    if gconf.DEBUG:
        print userData

    return userData

def lg(lCtrl=None, userData=[]):
    if lCtrl.logined:
        print s(u'已经在挂机中')
    else:
        for u in userData.itervalues():
            lCtrl.add_user(u['username'], u['password'])
        lCtrl.login()
        for u in userData.itervalues():
            u['status'] = lCtrl.users[u['username']]['status']
        p_user_data(userData)
    return userData

def rlg(lCtrl=None, userData=[]):
    if lCtrl.logined:
        lCtrl.logout()
    userData = lg(lCtrl, userData)
    return userData

if __name__ == '__main__':
    try:
        group_id = raw_input(s(u'请输入群号: '))

        if group_id != gconf.GROUP_ID:
            print s(u'抱歉！该工具仅限内部使用！')
            import time
            time.sleep(1)
            sys.exit(0)

        p_kotori()
        userData = lud()
        p_user_data(userData)

        lCtrl = login.LoginCtrl()

        while True:
            p_usage()
            cmd = raw_input(s(u'请输入命令: '))
            if cmd == 'a':
                userData = add_user(userData)
            elif cmd == 'd':
                userData = del_user(userData)
            elif cmd == 'p':
                p_user_data(userData)
            elif cmd == 'l':
                userData = lg(lCtrl, userData)
            elif cmd == 'r':
                userData = rlg(lCtrl, userData)
            elif cmd == 'q':
                break
        
    except KeyboardInterrupt:
        sys.exit(1)
