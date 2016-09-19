#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'

import json
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
"""
第二步，通过商户对应的菜品，与商户、经营范围映射表，匹配菜品名中包含经营范围的，输出商户名称, 经营范围，与对应的置信度
"""

# 商户、经营范围映射
range_shop_name_mapping_path = "/Users/Zealot/Desktop/waimai/shop_range_mapping"
#北京商户id，菜品名称
shop_dishes_info_path = "/Users/Zealot/Desktop/waimai/widDishTag.log"

#所有的经营范围

delimiter_blank = "\t"


def get_all_range():
    all_range = []
    for line in open(range_shop_name_mapping_path):
        shop_range = line.split("\t")[0]
        all_range.append(shop_range)
    return set(all_range)


def get_shop_id_name_dishes(file_path="shop_dishes_info.log"):
    """
    获取商户id，商户名称，菜品
    通过商户菜品的json文件中获取
    :return:
    """
    shop_id_products = []
    for line in open(file_path):
        shop_id = line.split(delimiter_blank)[0]
        shop_postfix = line.split(delimiter_blank)[1]
        products = []

        #所有的产品列表
        products = []
        # products_set = set(products)
        decodeb = json.loads(shop_postfix)
        for categoryId_name in decodeb:
            # print categoryId_name, decodeb[categoryId_name]
            for product_id_name in decodeb[categoryId_name]:
                p_name = product_id_name.split("_")[1]
                # products_set.add(p_name)
                products.append(p_name)

        shop_id_products.append((shop_id, products))
    return shop_id_products


def main():
    all_range = get_all_range()
    shop_id_products = get_shop_id_name_dishes(shop_dishes_info_path)
    fo = open("shop_id_range_rate3.txt", "w")
    for shop_id_product_set in shop_id_products:
        shop_id = shop_id_product_set[0]
        shop_product_set = shop_id_product_set[1]
        product_all_count = len(shop_product_set)
        if product_all_count == 0:
            continue
        product_set_str = "\t".join(shop_product_set)
        res_list = []
        for shop_range in all_range:
            # print shop_range
            product_count = product_set_str.count(shop_range)
            res_list.append((shop_range, float(product_count) / product_all_count))

        res = [shop_id]
        # print shop_id+"\t",
        for range_rate in res_list:
            range_r = range_rate[0] + "_" + str(range_rate[1])
            res.append(range_r)
            # print range_rate[0] + "_" + str(range_rate[1]) + "\t",
        fo.write("\t".join(res)+"\n")

if __name__ == '__main__':
    main()