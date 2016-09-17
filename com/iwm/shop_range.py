#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'

import MySQLdb

''''
商户转换成经营范围。一个商户会有多个标签，每个标签会对应一个权重。
1、通过商户id，找到商户名称，匹配到经营范围。
2、通过菜品名称，匹配到经营范围。
'''

delimiter_blank = " "


def get_shop_ids(file_path="shop_info.log"):
    """
    读取文件
    :return:得到每一个商户id，
    """
    shop_ids = []
    for line in open(file_path):
        shop_id = line.split(delimiter_blank)[0]
        shop_ids.append(shop_id)
        #print shop_id,
    return shop_ids


def get_shop_name_by_id(id):
    """
    通过sql查到每一个的商户名称。
    :param id:
    :return:
    """
    name = ""
    return name


def main():
    shop_ids = get_shop_ids()
    print shop_ids

if __name__ == '__main__':
    main()