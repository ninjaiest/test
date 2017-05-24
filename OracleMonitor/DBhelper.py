import cx_Oracle
sys.path.append("../")
import comm.getini as getini

class DBhelp():
	def __init__(self, password):
		self.username = getini.getini('./conf/conf.ini','DB','oracleuser','dba').replace('\n','')
		self.tnsname = getini.getini('./conf/conf.ini','DB','tnsname','orcl').replace('\n','')
		self.connstr = self.username + '/' + password + '@' + self.tnsname
		self.db = cx_Oracle.connect(self.connstr)		

	def executesql(self, sqlstr):
		cursor = self.db.cursor()
		cursor.execute(sqlstr)
		result = cursor.fetchall()
		return result

if __name__ == '__main__':
	dboper = DBhelp('123')
	sqlstr = 'select sysdate from dual'
	print dboper.executesql(sqlstr)
