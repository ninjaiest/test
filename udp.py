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
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ipaddr, port))
password, addr_tuple = s.recvfrom(1024)
s.sendto("recive password,program begin running!", addr_tuple)
s.close()

dbpasswd = password

dbmoni = OM.DBmonitor(dbpasswd)
print dbmoni.getstatus('cpu', 'key_cpu')
