#!/usr/bin/python
# -*- coding: utf-8 -*-

import cx_Oracle
import sys
import os
import time

sys.path.append("../")
import comm.getini as getini


class DBhelp:
    def __init__(self, password):
        self.runningdir = os.path.split(os.path.realpath(sys.argv[0]))[0]
        self.configfile = os.path.join(self.runningdir, 'conf', 'conf.ini')
        self.username = getini.getini(self.configfile, 'DB', 'oracleuser', 'dba').replace('\n', '')
        self.tnsname = getini.getini(self.configfile, 'DB', 'tnsname', 'orcl').replace('\n', '')
        self.connstr = self.username + '/' + password + '@' + self.tnsname
        self.db = None

    def executesql(self, sqlstrs):
        # starttime = time.time()
        self.db = cx_Oracle.connect(self.connstr)
        cursor = self.db.cursor()
        cursor.execute(sqlstrs)
        result = cursor.fetchall()
        self.db.close()
        # endtime = time.time()
        # print starttime, endtime - starttime
        return result


if __name__ == '__main__':
    dboper = DBhelp('123')
    sqlstr = 'select sysdate from dual'
    print dboper.executesql(sqlstr)
