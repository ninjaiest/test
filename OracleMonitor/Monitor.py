#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import DBhelper
import sqlite3
import comm.getini as getini

class DBmonitor():
	def __init__(self, password):
		self.runningdir = os.path.split(os.path.realpath(sys.argv[0]))[0]
		self.sqldir = os.path.join(self.runningdir,'conf','tmpsql')
		self.dboper = DBhelper.DBhelp(password)

	def test(self):
		sqlstr = "select sysdate from dual"
		result = self.dboper.executesql(sqlstr)
		return result

	def getAllKey(self):
		keylist = []
		conn = sqlite3.connect(os.path.join(self.runningdir,'conf','SQLdb','SQL.db'))
		cursor = conn.execute("SELECT * from MonitorItem")
		for keyline in cursor:
			keylist.append(list(keyline))
		return keylist

	def getbysql(self,onekeylist):
		sqlstr = ''
		for line in open(os.path.join(self.sqldir,onekeylist[3][7:]),'r').readlines():
			sqlstr += line
		print sqlstr





if __name__ == '__main__':
	dbmoni = DBmonitor('123')
	#print dbmoni.getvalues('cpu','key_cpu')
	dbmoni.getAllKey()
