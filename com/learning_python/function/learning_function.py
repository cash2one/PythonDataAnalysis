#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'


def printme(str):
    "打印传入的字符串到标准显示设备上"
    print str
    str = 456
    return


str = 123
printme(str)
print str
# 调用printme函数
printme(str="My string")


# 可写函数说明
def changeme(mylist):
    #修改传入的列表
    mylist.append([1, 2, 3, 4]);
    print "函数内取值: ", mylist
    return

# 调用changeme函数
mylist = [10, 20, 30];
changeme(mylist);
print "函数外取值: ", mylist

# 可写函数说明
def printinfo(name, age=35):
    "打印任何传入的字符串"
    print "Name: ", name
    print "Age ", age
    return

#调用printinfo函数
printinfo(age=50, name="miki")
printinfo(name="Jay")

# 不定长参数
def printinfo(arg1, *vartuple):
    #打印任何传入的参数
    print "输出: "
    print arg1
    for var in vartuple:
        print var
    return

# 调用printinfo 函数
printinfo(10)
printinfo(70, 60, 50)

#匿名函数lambda
sum = lambda arg1, arg2: arg1 + arg2
print "相加后的值为 : ", sum(10, 20)
print "相加后的值为 : ", sum(20, 20)