#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter

root = Tkinter.Tk()
root['bg'] = '#0099ff'
root.geometry("500x300+133+200")  # 设窗口大小  并初始化桌面位置

Label_key = Tkinter.Label(root, text="输入名称").grid(row=0, column=0)
# Label_key.pack(side=Tkinter.LEFT,anchor=Tkinter.W)

t_key = Tkinter.Text(root, width=50, height=1).grid(row=0, column=1)
# t_key.pack(side=Tkinter.TOP, anchor=Tkinter.W, fill=Tkinter.X, expand=Tkinter.YES,padx=1,pady=1)

Label_interval = Tkinter.Label(root, text="输入间隔").grid(row=1, column=0)
# Label_interval.pack(side=Tkinter.LEFT)

t_interval = Tkinter.Text(root, width=50, height=1).grid(row=1, column=1)
# t_interval.pack(side=Tkinter.TOP, anchor=Tkinter.W, fill=Tkinter.X, expand=Tkinter.YES)

Label_type = Tkinter.Label(root, text="输入类型").grid(row=2, column=0)
# Label_type.pack(side=Tkinter.LEFT)

t_type = Tkinter.Text(root, width=50, height=1).grid(row=2, column=1)
# t_type.pack(side=Tkinter.TOP, anchor=Tkinter.W, fill=Tkinter.X, expand=Tkinter.YES)

Label_cmd = Tkinter.Label(root, text="输入命令").grid(row=3, column=0)
# Label_cmd.pack(side=Tkinter.LEFT)

t_command = Tkinter.Text(root, width=50, height=5).grid(row=3, column=1)
# t_command.pack(side=Tkinter.TOP, anchor=Tkinter.W, fill=Tkinter.X, expand=Tkinter.YES)

b1 = Tkinter.Button(root, text="insert", width=10).grid(row=4, column=1)
# b1.pack(side=Tkinter.LEFT)

root.mainloop()
