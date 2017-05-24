import sys
import os
import cx_Oracle
sys.path.append("../")
import comm.getini as getini

class DBmonitor():
	def __init__(self, password):
		self.username = getini.getini('./conf/conf.ini','DB','oracleuser','dba').replace('\n','')
		self.tnsname = getini.getini('./conf/conf.ini','DB','tnsname','orcl').replace('\n','')
		self.connstr = self.username + '/' + password + '@' + self.tnsname

	def test(self):
		db = cx_Oracle.connect(self.connstr)
		cursor = db.cursor()
		sqlstr = "select * from v$version"
		cursor.execute(sqlstr)
		result = cursor.fetchall()
		print result

	def getstatus(self, typename, key):
		mydict = {}
		if typename == 'cpu':
			mydict[key] = 90
		return mydict

if __name__ == '__main__':
	dbmoni = DBmonitor('123')
	print dbmoni.getstatus('cpu','key_cpu')
