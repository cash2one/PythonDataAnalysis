#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'

"""
1.2（命中）:通过商户名称，与商户、经营范围映射表，得到商户id, 商户名称, 经营范围
北京地区
"""

# 商户、经营范围映射
range_shop_name_mapping_path = "/Users/Zealot/Desktop/waimai/shop_range_mapping_59"#又多加的7个类型
# 北京商户id，名称
shop_id_name_path = "/Users/Zealot/Desktop/waimai/beijing_wids"

# #所有的经营范围
# all_range = []
#{辅助词：经营范围}
all_range_map = {}
#
#
# def get_range_by_all_range(shop_name):
#     shop_range = ""
#     flag = False
#     for range_name in all_range:
#         if range_name in shop_name:
#             shop_range = range_name
#             flag = True
#     return shop_range, flag


def main():
    size = 0
    count = 0
    shop_name_and_range = {}
    for line in open(range_shop_name_mapping_path):
        fields = line.split("\t")
        shop_name = fields[1]
        # all_range.append(range)
        shop_name_and_range[shop_name] = range
        range_name = fields[0]
        for index in fields[1:]:
            if index.strip() != "" and index != "\t":
                all_range_map[index] = range_name

    fo = open("1009_1.2.txt", "w")
    print len(shop_name_and_range.keys())
    for line in open(shop_id_name_path):
        size += 1
        ss = line.split("\t")
        wid = ss[0]
        shop_name = ss[1]
        shop_range = ""

        for fuzhuci in all_range_map.keys():
            if shop_name.find(fuzhuci) != -1:
                shop_range = all_range_map[fuzhuci]

        if len(shop_range) > 0:
            count += 1
            fo.write(wid + "\t" + shop_name.replace("\n", "") + "\t" + shop_range + "\n")
    print size, count


if __name__ == '__main__':
    main()