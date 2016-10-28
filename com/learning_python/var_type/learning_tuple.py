#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'

def test():
    print "1"
def test():
    print "2"

#元组不能二次赋值，相当于只读列表
def main():
    # tuple = ('abcd', 786, 2.23, 'john', 70.2)
    # tinytuple = (123, 'john')
    #
    # print tuple  # 输出完整元组
    # print tuple[0]  # 输出元组的第一个元素
    # print tuple[1:3]  # 输出第二个至第三个的元素
    # print tuple[2:]  # 输出从第三个开始至列表末尾的所有元素
    # print tinytuple * 2  # 输出元组两次
    # print tuple + tinytuple  # 打印组合的元组
    # test()
    if 0:
        a = 1
        b = 2
        c = 3

    s = u"哈哈"
    r = u''+s
    print r

if __name__ == '__main__':
    main()