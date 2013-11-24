#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import uuid
import cPickle
import os
from gconf import GConf as gconf

class UserData(object):
    """stage1st session
    """


    def __init__(self):
        self.uuid = uuid.uuid3(uuid.NAMESPACE_DNS, gconf.BASE_URL)

    # encode a string password to big integer
    def _encode(self, password):
        res = 0
        b = 0
        mask = self.uuid.int
        for ch in password:
            res |= (ord(ch) ^ (mask & 255)) << b
            b += 8
            mask >>= 8
            if mask == 0:
                mask = self.uuid.int
        return res

    # decode a big integer into string password
    def _decode(self, enc_password):
        passwd = ''
        mask = self.uuid.int
        while enc_password > 0:
            ch = enc_password & 255
            passwd += chr(ch ^ (mask & 255))
            enc_password >>= 8
            mask = mask >> 8
            if mask == 0:
                mask = self.uuid.int
        return passwd

    # return a list of tuples (username, password)
    def load_user_data(self, filepath=None):
        if filepath is None:
            filepath = gconf.USER_DATA_PATH
        if not os.path.exists(filepath):
            f = open(filepath, 'wb')
            cPickle.dump([], f, 2)
            f.close()
        f = open(filepath, 'rb')
        try:
            encUserData = cPickle.load(f)
        except:
            raise Exception('Cannot pickle user data correctly. Please remove the user data file and retry.')
        return map(lambda (x,y): (x,self._decode(y)), encUserData)

    # user data should be a list of tuples (username, password)
    def save_user_data(self, userData, filepath=None):
        if filepath is None:
            filepath = gconf.USER_DATA_PATH
        encUserData = map(lambda (x,y): (x,self._encode(y)), userData)
        f = open(filepath, 'wb')
        cPickle.dump(encUserData, f, 2)
        f.close()

# test case
if __name__ == '__main__':
    ud = UserData()
    passwd='kotori@9my_little_angel狂三小天使@kula-fans'
    x = ud._encode(passwd)
    print x
    y = ud._decode(x)
    print y
    print y == passwd
    #ud.save_user_data([('test', passwd)])
    print ud.load_user_data()
