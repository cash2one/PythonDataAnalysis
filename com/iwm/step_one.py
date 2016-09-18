#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'

"""
第一步，通过商户名称，与商户、经营范围映射表，得到商户id, 商户名称, 经营范围
"""
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# 商户、经营范围映射
range_shop_name_mapping_path = "/Users/Zealot/Desktop/waimai/shop_range_mapping"
#北京商户id，名称
shop_id_name_path = "/Users/Zealot/Desktop/waimai/beijing_wids"

#所有的经营范围
all_range = []


def get_range_by_all_range(shop_name):
    shop_range = ""
    for range_name in all_range:
        if range_name in shop_name:
            shop_range = range_name.decode()
    return shop_range


def main():

    shop_name_and_range = {}
    for line in open(range_shop_name_mapping_path):
        range = line.split("\t")[0]
        shop_name = line.split("\t")[1]
        all_range.append(range)
        shop_name_and_range[shop_name] = range

    fo = open("shop_id_name_range.txt", "w")

    for line in open(shop_id_name_path):
        ss = line.split("\t")
        wid = ss[0]
        shop_name = ss[1].decode()

        # print all_range
        res = [wid]
        for range_name in all_range:
            if shop_name.find(range_name) != -1:
                res.append(shop_name_and_range[shop_name])

            fo.write("\t".join(res)+"\n")

        continue
        if shop_name in shop_name_and_range.keys():
            shop_range = shop_name_and_range[shop_name]
        else:
            # shop_range = get_range_by_all_range(shop_name)
            for range_name in all_range:
                if range_name in shop_name:
                    shop_range = range_name
                    fo.write("sss"+ shop_name)
        if len(shop_range) > 0:
            fo.write(wid + "\t" + shop_name.replace("\n", "") + "\t" + shop_range + "\n")

if __name__ == '__main__':
    main()