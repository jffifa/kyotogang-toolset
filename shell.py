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
        'ratelim':0,
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

def p_user_data(userData={}, showRatelim=True):
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
            print s(u'[今日评分限制: %d]') % (u[1]['ratelim'],)

def add_user(userData=[]):
    p_cutline()
    while True:
        username = t(raw_input(s(u'请输入用户名: '))).encode(gconf.INTERNAL_ENCODING)
        if len(username) > 0:
            break
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

        if username in userData:
            del userData[username]
            break
        else:
            uid = -1
            try:
                uid = int(username)
            except:
                pass

            if uid == 0:
                userData = {}
                break
            elif uid > 0 and uid <= len(userData):
                username = userData.values()[uid-1]['username']
                del userData[username]
                break
            else:
                print s(u'用户不存在')

    sud(userData)

    if gconf.DEBUG:
        print userData

    return userData

def lg(lCtrl=None, userData={}):
    if lCtrl.logined:
        print s(u'已经在挂机中')
    else:
        for u in userData.itervalues():
            lCtrl.add_user(u['username'], u['password'])
        lCtrl.login()
        for u in userData.itervalues():
            u['status'] = lCtrl.sessions[u['username']].status
        # get rate status
        r = rate.Rate()
        for s in lCtrl.sessions.itervalues():
            userData[s.username]['ratelim'] = r.get_rate_limit(s)
        p_user_data(userData)
    return userData

def rlg(lCtrl=None, userData={}):
    if lCtrl.logined:
        lCtrl.logout()
    userData = lg(lCtrl, userData)
    p_user_data(userData)
    return userData

def rate(lCtrl, userData):
    print s(u'欢迎使用评分核武器块')
    tid = 0
    floor = 0
    while True:
        try:
            tid = int(raw_input(s(u'请输入帖子id(帖子id就是帖子地址最后一段thread-xxxxxx-1-1.html中xxxxxx这个六位数字):')))
        except:
            pass
        if tid != 0:
            break
    while True:
        try:
            floor = int(raw_input(s(u'请输入楼号:')))
        except:
            pass
        if floor != 0:
            break
    while True:
        p_user_data(userData)
        username = t(raw_input(s(u'请输入用于评分的用户名或编号'))).encode(gconf.INTERNAL_ENCODING)

        if username not in userData:
            uid = -1
            try:
                uid = int(username)
            except:
                pass
            if uid > 0 and uid <= len(userData):
                username = userData.values()[uid-1]['username']
                break
        else:
            break

    if userData[username]['ratelim'] <= 0:
        print s(u'今日评分额度已用完')
        return userData

    session = lCtrl.sessions[username]
    r = Rate()

    pid, author = r.get_pid_author(session, tid, floor)
    if pid == 0:
        print s(u'无效帖子!')
        return userData

    print s(u'您要评分的对象是'),
    print author.decode(gconf.INTERNAL_ENCODING) # is there any codecs error?
    print s(u'扣鹅须谨慎，善恶一念存。中山公园外，一笑泯风尘。确认评分(y=是, n=否)'),
    while True:
        ch = raw_input('?')
        if ch == 'n':
            return userData
        else:
            break

    rateSgn = 0
    concurrency = 0
    while True:
        ch = raw_input(u'加鹅还是扣鹅?(输入+加鹅,输入-扣鹅):')
        if ch == '+':
            rateSgn = 1
            break
        else:
            rateSgn = -1
            break
    while True:
        try:
            concurrency = int(raw_input(u'请输入并发数(数字越大账面加/扣分越多,最大256)'))
            if concurrency > 0 and concurrency <= gconf.MAX_RATE_CONCURRENCY:
                break
        except:
            pass
    
    formtable = r.get_formtable(session, tid, pid) 
    if formtable is None:
        print s(u'无效帖子!')
        return userData

    rateRes = r.rate(session=session, rateSgn=rateSgn, c=concurrency, tid=tid, pid=pid, formtable=formtable)

    if rateRes:
        print s(u'评分成功')
    else:
        print s(u'评分失败')

    userData[username]['ratelim'] = r.get_rate_lim(session)
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
            elif cmd == 'h':
                userData = rate(lCtrl, userData)
            elif cmd == 'q':
                break
        
    except KeyboardInterrupt:
        sys.exit(1)
