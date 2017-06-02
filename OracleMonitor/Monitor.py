#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import DBhelper
import sqlite3
import time
import threading
import thread

keylist = []


class DBmonitor:
    def __init__(self, password, sqlitecnn):
        global keylist
        global lock
        self.runningdir = os.path.split(os.path.realpath(sys.argv[0]))[0]
        self.sqldir = os.path.join(self.runningdir, 'conf', 'tmpsql')
        self.dboper = DBhelper.DBhelp(password)
        keylist = self.getAllKey()
        lock = thread.allocate_lock()
        self.con = sqlitecnn
        self.isfirst = 1

    def test(self):
        sqlstr = "select sysdate from dual"
        result = self.dboper.executesql(sqlstr)
        return result

    def getAllKey(self):
        inittime = time.time()
        vkeylist = []
        conn = sqlite3.connect(os.path.join(self.runningdir, 'conf', 'SQLdb', 'SQL.db'))
        cursor = conn.execute("SELECT * from MonitorItem")
        for keyline in cursor:
            tmplist = list(keyline)
            tmplist.append(inittime)
            tmplist.append(0)
            tmplist.append(0)
            tmplist.append(0)
            vkeylist.append(tmplist)
        return vkeylist

    def getbysql(self, onekeylist):
        sqlstr = ''
        for line in open(os.path.join(self.sqldir, onekeylist[3][7:]), 'r').readlines():
            sqlstr += line
        return sqlstr

    def getItemValuebytread(self, skey):
        if skey[2] == 'sql':
            if skey[3][:7] == 'infile:':
                skey[5] = self.dboper.executesql(self.getbysql(skey))[0][0]
                skey[4] = time.time()
                skey[6] = 1
                skey[7] = 0
                self.opersqlite(skey)
        if skey[2] == 'command':
            skey[5] = '123213213213213'
            skey[4] = time.time()
            skey[6] = 1
            skey[7] = 0
            self.opersqlite(skey)

    def opersqlite(self, skeylist):
        cur = self.con.cursor()
        cur.execute("delete from keyvalues where key='" + skeylist[0] + "'")
        assert isinstance(cur, object)
        cur.execute("insert into keyvalues(key,lastrungtime,keyvalues,isupdate,isSend) values('" + skeylist[0] + "'," +
                    str(skeylist[4]) + ",'" + skeylist[5] + "'," + str(skeylist[6]) + "," + str(skeylist[7]) + ")")
        # print cur.fetchall()

    def getItemRun(self):
        if self.isfirst == 0:
            self.getItemValue()
        elif self.isfirst == 1:
            self.getItemValuefirst()

    def getItemValue(self):
        global keylist
        for skey in keylist:
            if time.time() - skey[4] >= skey[1]:
                global lock
                # lock.acquire()
                t = threading.Thread(target=self.getItemValuebytread, args=(skey,))
                t.start()
                t.join()
                # lock.release()
                # t.join()

    def getItemValuefirst(self):
        global keylist
        for skey in keylist:
            global lock
            # lock.acquire()
            t = threading.Thread(target=self.getItemValuebytread, args=(skey,))
            t.start()
            t.join()
            # lock.release()
            # t.join()
        self.isfirst = 0

    def getdatefromsqlite(self):
        pass

if __name__ == '__main__':
    dbmoni = DBmonitor('123')
    # print dbmoni.getvalues('cpu','key_cpu')
    dbmoni.getAllKey()
