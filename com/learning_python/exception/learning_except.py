#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'

try:
    fh = open("testfile", "w")
    fh.write("这是一个测试文件，用于测试异常!!")
except IOError:
    print "Error: 没有找到文件或读取文件失败"
else:
    #如果在try子句执行时没有发生异常，python将执行else语句后的语句（如果有else的话），然后控制流通过整个try语句。
    print "内容写入文件成功"
    fh.close()

#try-finally 语句无论是否发生异常都将执行最后的代码。
try:
    fh = open("testfile", "w")
    fh.write("这是一个测试文件，用于测试异常!!")
finally:
    print "Error: 没有找到文件或读取文件失败"