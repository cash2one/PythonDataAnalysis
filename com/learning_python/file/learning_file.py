#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'

import time  # 引入time模块

ticks = time.time()
print "当前时间戳为:", ticks
fo = open("hello", "r")

# str = fo.read(11)
# print str
index = 0
for line in open("hello"):
    index += 1

ticks2 = time.time()
print "当前时间戳为:", ticks2
print "总时长:", ticks2 - ticks
print "index: ", index


"""
带缓存的文件读取
"""
file = open("hello")

ticks3 = time.time()
index = 0
while 1:
    lines = file.readlines(100000)
    if not lines:
        break
    for line in lines:
        index += 1
ticks4 = time.time()
print "总时长:", ticks4 - ticks3