#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json

fp = open('../conf/MonitorSQL.ini','r')
d = json.loads(fp.read())
print d, type(d)
print d['DBbase'][1]

