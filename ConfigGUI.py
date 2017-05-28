#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter

root = Tkinter.Tk()
root['bg'] = '#0099ff'
root.geometry("1024x300+133+200")         #设窗口大小  并初始化桌面位置
t = Tkinter.Text(root, width=100, height=20)
t.pack(side=Tkinter.LEFT)
b1 = Tkinter.Button(root, text="insert", width=10)
b1.pack(side=Tkinter.LEFT)
root.mainloop()