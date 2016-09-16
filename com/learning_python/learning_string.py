#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'


def main():
    a = 1
    b = 2
    x = a + b
    print x

    imperative = "abc"
    expletive = "123"
    s = '%s, %s!' % (imperative, expletive)
    print s
    x = '{}, {}!'.format(imperative, expletive)
    print x
    name = "eminem阿姆"
    n = 1
    s2 = 'name: %s; score: %d' % (name, n)
    print s2
    s3 = 'name: {}; score: {}'.format(name, n)
    print s3
    s4 = 'name: ' + name + '; score: ' + str(n)
    print s4

    str1 = 'Hello World!'

    print str1  # 输出完整字符串
    print str1[0]  # 输出字符串中的第一个字符
    print str1[2:5]  # 输出字符串中第三个至第五个之间的字符串
    print str1[2:]  # 输出从第三个字符开始的字符串
    print str1 * 2  # 输出字符串两次
    print str1 + "TEST"  # 输出连接的字符串

if __name__ == '__main__':
    main()