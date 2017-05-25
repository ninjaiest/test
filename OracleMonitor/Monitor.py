#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import DBhelper
sys.path.append("../")
import comm.getini as getini

class DBmonitor():
	def __init__(self, password):
		self.dboper = DBhelper.DBhelp(password)

	def test(self):
		sqlstr = "select sysdate from dual"
		result = self.dboper.executesql(sqlstr)
		return result

	def getvalues(self, typename, key):
		mydict = {}
		if typename == 'cpu':
			mydict[key] = 90
		if typename == 'tablesspace':
			sqlstr = '''
			SELECT  d.tablespace_name "Name", d.status "Status", d.contents "Type", 
			TO_CHAR(NVL(a.bytes / 1024 / 1024, 0),'99G999G990D900') "Size (MB)", 
			TO_CHAR(NVL(a.bytes - NVL(f.bytes, 0),0)/1024/1024, '99G999G990D900') "Used (MB)", 
			TO_CHAR(NVL((a.bytes - NVL(f.bytes, 0)) / a.bytes * 100, 0), '990D00') "Used％" 
			from sys.dba_tablespaces d,
			(select tablespace_name, sum(bytes) bytes 
			from dba_data_files group by tablespace_name) a, 
			(select tablespace_name, sum(bytes) bytes 
			from dba_free_space group by tablespace_name) f  
			WHERE d.tablespace_name = a.tablespace_name(+) 
			AND d.tablespace_name = f.tablespace_name(+) and d.tablespace_name = 'USERS'
			'''
			print sqlstr
			result = self.dboper.executesql(sqlstr)
			mydict[key] = result[0][5].strip()
			# return result


		return mydict



if __name__ == '__main__':
	dbmoni = DBmonitor('123')
	print dbmoni.getvalues('cpu','key_cpu')
