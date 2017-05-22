import sys
import random
import time
import socket

ipaddr = '127.0.0.1'
port = 12582
password = ''
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

fp = open("neo.txt","a+")
while True:
	fp.writelines(password + "this is the random number:" + str(random.randrange(0,9)) + '\n' )
	fp.flush()
	time.sleep(3)

