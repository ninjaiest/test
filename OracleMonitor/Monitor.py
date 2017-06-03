#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import DBhelper
import sqlite3
import time
import threading

keylist = []  # 全局列表 用于存储所有配置项的KEY列表，keylist中的每个列表包含 key，间隔，类型，命令，运行时间，值，更新，发送
dictKeyTreadRunStatus = {}  # 全局字典 存储获取KEY值时的线程状态


class DBmonitor:
    def __init__(self, password, sqlitecnn):
        global keylist
        self.runningdir = os.path.split(os.path.realpath(sys.argv[0]))[0]
        self.sqldir = os.path.join(self.runningdir, 'conf', 'tmpsql')
        self.dboper = DBhelper.DBhelp(password)
        keylist = self.getAllKey()
        self.con = sqlitecnn
        self.isfirst = 1

    def getAllKey(self):
        """
        初始化 keylist
        :return:返回更新后的keylist
        """
        inittime = time.time()
        vkeylist = []
        conn = sqlite3.connect(os.path.join(self.runningdir, 'conf', 'SQLdb', 'SQL.db'))
        cursor = conn.execute("SELECT * from MonitorItem")
        for keyline in cursor:
            tmplist = list(keyline)
            tmplist.append(inittime)  # 运行时间
            tmplist.append(0)  # 获取的值
            tmplist.append(0)  # 是否已更新
            tmplist.append(0)  # 是否已发送
            vkeylist.append(tmplist)
        return vkeylist

    def GetSqlbyFile(self, onekeylist):
        """
        获取SQL文件中的SQL语句
        :param onekeylist:
        :return:
        """
        sqlstr = ''
        for line in open(os.path.join(self.sqldir, onekeylist[3][7:]), 'r').readlines():
            sqlstr += line
        return sqlstr

    def opersqlite(self, skeylist):
        """
        更新sqlite中的监控数据状态，同时确保sqlite中每个KEY的监控值数据小于等于1条
        :param skeylist:
        :return:
        """
        cur = self.con.cursor()
        cur.execute("select count(1) from keyvalues where key='" + skeylist[0] + "'")
        datalist = cur.fetchall()
        if datalist[0][0] > 0:
            cur.execute("update keyvalues set lastrungtime=" + str(skeylist[4]) + ", keyvalues='" + skeylist[
                5] + "', isSend=0 where key='" + skeylist[0] + "'")
        else:
            cur.execute(
                "insert into keyvalues(key,lastrungtime,keyvalues,isupdate,isSend) values('" + skeylist[0] + "'," + str(
                    skeylist[4]) + ",'" + skeylist[5] + "'," + str(skeylist[6]) + "," + str(skeylist[7]) + ")")
        cur.close()

    def getValuefirst(self):
        """
        第一次获取监控项值时的多线程操作
        :return:
        """
        global keylist
        for skey in keylist:
            t = threading.Thread(target=self.getValuebytread, args=(skey,))
            t.start()
            t.join()
        self.isfirst = 0

    def getValuenotfirst(self):
        """
        非第一次获取监控项值时多线程操作

        :return:
        """
        global keylist
        for skey in keylist:
            # 检查在线程状态字典中 是否存在该KEY
            if skey[0] in dictKeyTreadRunStatus:
                cur = self.con.cursor()
                cur.execute("select isSend from keyvalues where key='" + skey[0] + "' and lastrungtime=" + str(skey[4]))
                if cur.fetchall():
                    dictKeyTreadRunStatus.pop(skey[0])
                cur.close()
            else:
                if time.time() - skey[4] >= skey[1]:
                    skey[4] = time.time()  # 必须在这里更新执行时间，如果在线程中去更新时间，线程执行瞬间会在此打开N多新线程
                    dictKeyTreadRunStatus[skey[0]] = 1
                    t = threading.Thread(target=self.getValuebytread, args=(skey,))
                    t.start()

    def getValuebytread(self, skey):
        """
        获取监控项的值
        :param skey:
        :return:
        """
        if skey[2] == 'sql':
            if skey[3][:7] == 'infile:':
                skey[5] = self.dboper.executesql(self.GetSqlbyFile(skey))[0][0]
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

    def getItemRun(self):
        """
        运行主函数
        :return:
        """
        if self.isfirst == 0:
            self.getValuenotfirst()
        elif self.isfirst == 1:
            self.getValuefirst()


if __name__ == '__main__':
    con = sqlite3.connect(":memory:", check_same_thread=False)
    dbmoni = DBmonitor('123', con)
    # print dbmoni.getvalues('cpu','key_cpu')
    dbmoni.getAllKey()
