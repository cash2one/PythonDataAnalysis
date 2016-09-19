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

    err_html = '''
    <HTML><HEAD><TITLE>
    Friends CGI Demo</TITLE></HEAD>
    <BODY><H3>ERROR</H3>
    <B>%s</B><P>
    <FORM><INPUT TYPE=button VALUE=Back
    ONCLICK="window.history.back()"></FORM>
    </BODY></HTML>
    '''
    print err_html

    str3 = "http://www.w3cschool.cc/"
    print str3.partition("://")
    str2 = "123_test"
    print str2.partition("_")
    ss = str2.split("_")
    print ss[0], ss[1]
    print str3.count("c")
    print 123, 456,
    print 789
if __name__ == '__main__':
    main()