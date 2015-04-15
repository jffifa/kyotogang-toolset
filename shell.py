#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
from kotori import *
from kotori.gconf import GConf as gconf
import sys
import getpass
import time
import os
import platform

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
    kotoriPath = os.path.join(gconf.BASE_DIR, gconf.KOTORI_ASCII_PATH)
    f = open(kotoriPath, 'r')
    str_kotori = f.read()
    f.close()
    # detect os platform
    if platform.system() == 'Windows':
        os.system('mode con: cols=%d lines=%d' % (89, 512))
        print str_kotori
    else:
        print str_kotori
    time.sleep(2.5)

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
    h: 评分核武
    p: 显示当前已经添加的用户列表
    q: 退出"""
    print s(usg)

def p_user_data(userList, userData, rateLim=False):
    p_cutline()
    print s(u'当前已添加的用户列表:')
    if len(userList) == 0:
        print s(u'无')
    else:
        for i in xrange(len(userList)):
            if rateLim and userData[userList[i]]['ratelim']<=0:
                continue
            else:
                print str(i+1)+'>', s(userData[userList[i]]['username'].decode(gconf.INTERNAL_ENCODING)),
                if userData[userList[i]]['status'] == gconf.SESSION_STATUS_LOGIN:
                    print s(u'[已登录]'),
                else:
                    print s(u'[未登录]'),
                print s(u'[今日评分限制: %d]') % (userData[userList[i]]['ratelim'],)

def parse_un(us, userList, userData):
    if us not in userData:
        uid = -1
        try:
            uid = int(us)
        except:
            return None
        if uid > 0 and uid <= len(userList):
            return userList[uid-1]
        else:
            return None
    else:
        return us
    return None

def add_user(userList, userData):
    if len(userList) >= gconf.MAX_USER:
        print s(u'已达到用户数上限制!')
        return None
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
                break
    else:
        userData[username] = gnu(username, password)
        userList.append(username)

    sud(userData)

    if gconf.DEBUG:
        print userData

def del_user(userList, userData):
    while True:
        p_user_data(userList, userData)
        username = t(raw_input(s(u'请输入用户编号或用户名(0表示清空, 直接回车取消): '))).encode(gconf.INTERNAL_ENCODING)

        username = parse_un(username, userList, userData)
        if username is None:
            print s(u'用户不存在')
        else:
            del userData[username]
            userList.remove(username)
            break

    sud(userData)

    if gconf.DEBUG:
        print userData

def lg(lCtrl, userList, userData):
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
        for session in lCtrl.sessions.itervalues():
            userData[session.username]['ratelim'] = r.get_rate_limit(session)
        p_user_data(userList, userData)

def rlg(lCtrl, userList, userData):
    if lCtrl.logined:
        lCtrl.logout()
    userData = lg(lCtrl, userList, userData)

def dorate(lCtrl, userList, userData):
    if not lCtrl.logined:
        print s(u'尚未登录,不能评分!')
        return
    print s(u'欢迎使用评分核武模块')
    print
    tid = 0
    floor = 0
    while True:
        try:
            tid = int(raw_input(s(u'请输入帖子id\n(帖子id就是帖子地址最后一段thread-xxxxxx-1-1.html中xxxxxx这个六位数字): ')))
        except:
            pass
        if tid != 0:
            break
    while True:
        try:
            floor = int(raw_input(s(u'请输入楼号: ')))
        except:
            pass
        if floor != 0:
            break

    r = rate.Rate()

    pid, author = r.get_pid_author(tid, floor)
    if pid == 0:
        print s(u'无效帖子!')
        return

    print
    print s(u'您要评分的对象是'),
    print author.decode(gconf.INTERNAL_ENCODING) # is there any codecs error?
    print s(u'扣鹅须谨慎，善恶一念存。中山公园外，一笑泯风尘。确认评分(y=是, n=否)'),
    while True:
        ch = raw_input('?')
        if ch == 'n':
            return
        elif ch == 'y':
            break

    usernames = []
    while True:
        p_user_data(userList=userList, userData=userData, rateLim=True)
        _hint = u'请输入用于评分的用户名或编号\n(如果想队形队形就输入多个帐号,账号间用空格隔开): '
        unstr = t(raw_input(s(_hint))).encode(gconf.INTERNAL_ENCODING).strip()
        un = unstr.split(' ')

        flag = True
        for username in un:
            username = parse_un(username, userList, userData)
            if username is None:
                flag = False
                break
            else:
                usernames.append(username)
        if flag == False:
            print s(u'输入非法')
        else:
            break

    sessions = []
    for username in usernames:
        if userData[username]['status'] != gconf.SESSION_STATUS_LOGIN:
            print s(u'帐号 %s 尚未登录') % username
            return
        elif userData[username]['ratelim'] <= 0:
            print s(u'帐号 %s 今日评分额度已用完') % username
            return
        else:
            sessions.append(lCtrl.sessions[username])

    rateSgn = 0
    concurrency = 0
    while True:
        ch = raw_input(s(u'加鹅还是扣鹅?(输入+加鹅,输入-扣鹅): '))
        if ch == '+':
            rateSgn = 1
            break
        elif ch == '-':
            rateSgn = -1
            break
        else:
            pass
    while True:
        try:
            concurrency = int(raw_input(s(u'请输入并发数(数字越大账面加/扣分越多,最大%d): ')%(gconf.MAX_RATE_CONCURRENCY,)))
            if concurrency > 0 and concurrency <= gconf.MAX_RATE_CONCURRENCY:
                break
        except:
            pass

    rateReasons = []
    while True:
        _hint = u'请输入加/扣鹅理由\n(如果想队形评分就输入多个理由,理由间用空格隔开,数量必须和之前输入的用户数相同): '
        reasonstr = t(raw_input(s(_hint))).encode(gconf.INTERNAL_ENCODING).strip()
        rateReasons = reasonstr.split(' ')

        if len(rateReasons) == len(sessions):
            break
        else:
            continue

    page = r.get_page(floor=floor) # dirty hack?
    rateRes = r.multi_rate(sessions=sessions, rateSgn=rateSgn, rateReasons=rateReasons, c=concurrency, tid=tid, pid=pid, page=page)

    if rateRes:
        print s(u'评分成功')
    else:
        print s(u'评分失败')

    for username, session in zip(usernames, sessions):
        userData[username]['ratelim'] = r.get_rate_limit(session)

if __name__ == '__main__':
    try:
        group_id = raw_input(s(u'请输入群号: ')).strip()

        if group_id != gconf.GROUP_ID:
            print s(u'抱歉！该工具仅限内部使用！')
            import time
            time.sleep(1)
            sys.exit(0)

        p_kotori()
        userData = lud()
        userList = [u['username'] for u in userData.itervalues()]
        p_user_data(userList, userData)

        lCtrl = login.LoginCtrl()

        while True:
            p_usage()
            cmd = raw_input(s(u'请输入命令: '))
            if cmd == 'a':
                add_user(userList, userData)
            elif cmd == 'd':
                del_user(userList, userData)
            elif cmd == 'p':
                p_user_data(userList, userData)
            elif cmd == 'l':
                lg(lCtrl, userList, userData)
            elif cmd == 'r':
                rlg(lCtrl, userList, userData)
            elif cmd == 'h':
                dorate(lCtrl, userList, userData)
            elif cmd == 'q':
                break
        
    except KeyboardInterrupt:
        sys.exit(1)
