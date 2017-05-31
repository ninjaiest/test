#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import time
import socket
import comm.getini as getini
import OracleMonitor.Monitor as OM

ipaddr =  getini.getini('./conf/conf.ini','GetPasswd','ipaddres','localhost')
port = int(getini.getini('./conf/conf.ini','GetPasswd','port','3389'))

# use tcp mode
'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ipaddr,port))
s.listen(10)
conn, addr = s.accept()
password = conn.recv(1024)
conn.send("recive the password is:" + str(password))
time.sleep(5)
s.shutdown(2)
s.close()
'''

#u use udp mode
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s.bind((ipaddr, port))
#password, addr_tuple = s.recvfrom(1024)
#s.sendto("recive password,program begin running!", addr_tuple)
#s.close()

dbpasswd = '#EDC2wsx1qaz189'

dbmoni = OM.DBmonitor(dbpasswd)
# print dbmoni.getvalues('cpu', 'key_cpu')
# print dbmoni.test()
#tbspace = dbmoni.getvalues('tablesspace', 'tbs_user_used')
l = dbmoni.getAllKey()
for k in l:
	if k[2] == 'sql':
		dbmoni.getbysql(k)
