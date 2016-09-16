#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'


def main():
    dict = {}
    dict['one'] = "This is one"
    dict[2] = "This is two"

    tinydict = {'name': 'john', 'code': 6734, 'dept': 'sales'}

    print dict['one']  # 输出键为'one' 的值
    print dict[2]  # 输出键为 2 的值
    print tinydict  # 输出完整的字典
    print tinydict.keys()  # 输出所有键
    print tinydict.values()  # 输出所有值
    print tinydict.keys()[1:2]
    print "one" in dict

    #修改字典
    dict2 = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}

    dict2['Age'] = 8  # update existing entry
    dict2['School'] = "DPS School"  # Add new entry

    print "dict2['Age']: ", dict2['Age']
    print "dict2['School']: ", dict2['School']

    del dict2['Name']  # 删除键是'Name'的条目
    #清空词典所有条目
    dict2.clear()
    #删除词典
    del dict2

    print "dict2['Age']: ", dict2['Age']
    print "dict2['School']: ", dict2['School']

if __name__ == '__main__':
    main()