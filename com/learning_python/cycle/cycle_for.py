#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'

for letter in 'Python':  # 第一个实例
    print '当前字母 :', letter

fruits = ['banana', 'apple', 'mango']
for fruit in fruits:  # 第二个实例
    print '当前字母 :', fruit

print "Good bye!"

#通过序列索引迭代
fruits = ['banana', 'apple',  'mango']
for index in range(len(fruits)):
    print '当前水果 :', fruits[index]

print "Good bye!"

#for 中的语句和普通的没有区别，else 中的语句会在循环正常执行完
for num in range(10, 20):  # 迭代 10 到 20 之间的数字
    for i in range(2, num):  # 根据因子迭代
        if num % i == 0:  # 确定第一个因子
            j = num / i  # 计算第二个因子
            print '%d 等于 %d * %d' % (num, i, j)
            break  # 跳出当前循环
    else:  # 循环的 else 部分
        print num, '是一个质数'

# 输出 Python 的每个字母,Python pass是空语句，是为了保持程序结构的完整性。
#pass 不做任何事情，一般用做占位语句。
for letter in 'Python':
    if letter == 'h':
        pass
        print '这是 pass 块'
    print '当前字母 :', letter

print "Good bye!"