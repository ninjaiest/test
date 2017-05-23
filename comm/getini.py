#!/usr/bin/python
# -*- coding: UTF-8 -*-
#读取INI 配置文件函数
def getini (iniFile ,mainKey ,subKey ,Defvalues ):
    FindMainKey=None
    FindSubKey=None
    for line in open (iniFile ):
        if FindMainKey ==None:
            if line .find ('['+ mainKey+']')==0 :
                FindMainKey =1
        else:
            if line .find ('[')== 0:
                return Defvalues
            if line .find (subKey +'=')== 0:
                FindSubKey =1
                return line [line .find ('='):]. replace('=','' )
    if FindMainKey ==None or FindSubKey ==None:
        return Defvalues
