#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'

# 打开一个文件
fo = open("foo.txt", "wb")
fo.write("www.runoob.com!\nVery good site!\n")

# 关闭打开的文件
fo.close()