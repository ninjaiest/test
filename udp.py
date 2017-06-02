#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import random
import time
import socket
import sqlite3
import threading
import comm.getini as getini
import OracleMonitor.Monitor as Om

runningdir = os.path.split(os.path.realpath(sys.argv[0]))[0]
ipaddr = getini.getini(os.path.join(runningdir, 'conf', 'conf.ini'), 'GetPasswd', 'ipaddres', 'localhost')
port = int(getini.getini(os.path.join(runningdir, 'conf', 'conf.ini'), 'GetPasswd', 'port', '3389'))

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

# u use udp mode
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.bind((ipaddr, port))
# password, addr_tuple = s.recvfrom(1024)
# s.sendto("recive password,program begin running!", addr_tuple)
# s.close()

dbpasswd = '#EDC2wsx1qaz189'

con = sqlite3.connect(":memory:", check_same_thread=False)
cur = con.cursor()
cur.executescript("""
create table keyvalues(
key varchar(20),
lastrungtime float,
keyvalues text,
isupdate int,
isSend int)""")
cur.close()

dbmoni = Om.DBmonitor(dbpasswd, con)
while True:
    l = dbmoni.getItemRun()
    cur = con.cursor()
    cur.execute('select * from keyvalues where isupdate=1 and isSend<>1')
    lists = cur.fetchall()

    if len(lists) > 0:
        print lists

    cur.execute("update keyvalues set isSend=1 where isupdate=1")
    cur.close()
    time.sleep(5)
