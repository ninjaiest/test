#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import sqlite3
from tabulate import tabulate

class configkey():
	def __init__(self):
		self.runningdir = os.path.split(os.path.realpath(sys.argv[0]))[0]
		self.conn = sqlite3.connect(os.path.join(self.runningdir,'conf','SQLdb','SQL.db'))
		print "Opened database successfully"

	def createtb(self):
		'''
		key:
		interval:
		type:
		sql/command:
		'''
		self.conn.execute(
		'''
		create table if not exists MonitorItem (
		key VARCHAR[20],
		interval int,
		type varchar[10],
		command text
		) 
		'''
		)
		print "create or table successfully"

	def selectcommand(self):
		while True:
			print "==please choose the follow items:"
			print "\t1:show data"
			print "\t2:add key itme"
			print "\t3:modify the item"
			print "\t4:delete the item"
			print "\t5:exit program"
			cs = raw_input("your choose is:")
			if cs.isdigit() == True:
				return int(cs)

	def showdata(self):
		print "==show the all config key as follow:"
		cursor = self.conn.execute("SELECT * from MonitorItem")
		#for l in cursor.fetchall():
		#	print l
		#print tabulate(cursor.description(), tablefmt="grid")
		colnamelist = []
		colnamelist_t = []
		values = []
		for colname in cursor.description:
			colnamelist_t.append(colname[0])
		colnamelist.append(tuple(colnamelist_t))

		for l_values in cursor.fetchall():
			colnamelist.append(l_values)

		print tabulate(colnamelist, tablefmt="grid")

	def insertitem(self):
		vkey = raw_input("key:")
		vinterval = int(raw_input("interval:"))
		vtype = raw_input("type:")
		command = raw_input("command:")
		self.conn.execute("INSERT INTO MonitorItem (key, interval, type,command) VALUES ('" + vkey + "', " + str(vinterval) + ",'" +  vtype + "', '" + command + "')");
		self.conn.commit()

	def deleteitembykey(self):
		vkey = raw_input("please input the key you want to del:")
		self.conn.execute("delete from MonitorItem where key = '" + vkey + "'")
		self.conn.commit()

	def updateitembykey(self):
		vkey = raw_input("please input the key you want to update:")
		print "the date you will be update is follow:"
		cursor = self.conn.execute("SELECT * from MonitorItem where key='" + vkey +"'")
		colnamelist = []
		colnamelist_t = []
		values = []
		for colname in cursor.description:
			colnamelist_t.append(colname[0])
		colnamelist.append(tuple(colnamelist_t))

		for l_values in cursor.fetchall():
			colnamelist.append(l_values)

		print tabulate(colnamelist, tablefmt="grid")

		newinterval = ''
		while newinterval.isdigit() == False:
			newinterval = raw_input("please input the new interval:")	
			if newinterval.strip() == '':
				newinterval = str(l_values[1])
		newinterval = int(newinterval)

		newtype = raw_input("please input the new type:")
		if newtype.strip() == '':
			newtype = l_values[2]

		newcommand = raw_input("please input the new command:")
		if newcommand.strip() == '':
			newcommand = l_values[3]


		self.conn.execute("update MonitorItem set interval=" + str(newinterval) + ", type ='" + newtype + "', command = '" + newcommand + "' where key='" + vkey + "'")
		self.conn.commit()

if __name__ == '__main__':
	operconfig = configkey()
	while True:
		cs = operconfig.selectcommand()
		if cs == 5:
			sys.exit()
		if cs == 1:
			operconfig.showdata()
		if cs == 2:
			operconfig.insertitem()
		if cs == 3:
			operconfig.updateitembykey()
		if cs == 4:
			operconfig.deleteitembykey()

	