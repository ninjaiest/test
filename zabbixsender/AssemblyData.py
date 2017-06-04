#!/usr/bin/env python

import sqlite3
import os
import sys

skeylist = []


class assembly:
    def __init__(self, con):
        global skeylist
        self.runningdir = os.path.split(os.path.realpath(sys.argv[0]))[0]
        self.conn = sqlite3.connect(os.path.join(self.runningdir, 'conf', 'SQLdb', 'SQL.db'))
        self.cursor = self.conn.execute("SELECT * from MonitorItem")
        for keyline in self.cursor:
            skeylist.append(list(keyline))
        self.conMemSqlite = con

    def assemblybykey(self):
        cur = self.conMemSqlite.cursor()
        for skey in skeylist:
            cur.execute("select * from keyvalues where key='" + skey[0] + "' and isSend=0")
            ret = cur.fetchall()
            if 0 < len(ret):
                cur.execute("update keyvalues set isSend=1 where key='" + skey[0] + "' and isSend=0")
                print ret





