#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'


#判断条件可以是任何表达式，任何非零、或非空（null）的值均为true。
#当判断条件假false时，循环结束。

count = 0
while count < 9:
    print 'The count is:', count
    count += 1

print "Good bye!"

# continue 和 break 用法

i = 1
while i < 10:
    i += 1
    if i % 2 > 0:  # 非双数时跳过输出
        continue
    print i  # 输出双数2、4、6、8、10

i = 1
while 1:  # 循环条件为1必定成立
    print i  # 输出1~10
    i += 1
    if i > 10:  # 当i大于10时跳出循环
        break

count = 0
while count < 5:
    print count, " is  less than 5"
    count = count + 1
else:
    print count, " is not less than 5"

flag = 1
#一行进行书写
#while flag: print 'Given flag is really true!'

print "Good bye!"