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
range_shop_name_mapping_path = "/Users/Zealot/Desktop/waimai/shop_range_mapping_110"
# range_shop_name_mapping_path = "/Users/Zealot/Desktop/waimai/shop_range_mapping_17"
#所有商户id，菜品名称
shop_dishes_info_path = "/Users/Zealot/Desktop/waimai/widDishTag.log"
#北京商户id，名称
# shop_dishes_info_path = "/Users/Zealot/Desktop/waimai/beijing_wids"

output = "/Users/Zealot/Desktop/waimai/shop_id_range_rate_0927_2.txt"

#所有的经营范围

delimiter_blank = "\t"


def get_all_range():
    """
    获取所有的经营范围
    :return:
    """
    all_range = []
    for line in open(range_shop_name_mapping_path):
        shop_range = line.strip().split("\t")[0]
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


def get_all_dishes(file_path="shop_dishes_info.log"):
    """
    获取所有菜品
    :return:
    """
    fo = open("/Users/Zealot/Desktop/waimai/all_dishes.txt", "w")
    for line in open(file_path):
        shop_id = line.split(delimiter_blank)[0]
        shop_postfix = line.split(delimiter_blank)[1]
        products = []

        decodeb = json.loads(shop_postfix)
        for categoryId_name in decodeb:
            for product_id_name in decodeb[categoryId_name]:
                p_name = product_id_name.split("_")[1]
                fo.write(p_name+"\n")
    fo.close()


def get_range_by_dish_name(all_range, shop_id_products):
    fo = open(output, "w")
    for shop_id_product_set in shop_id_products:
        shop_id = shop_id_product_set[0]
        shop_product_set = shop_id_product_set[1]
        product_all_count = len(shop_product_set)
        if product_all_count == 0:
            continue
        product_set_str = "\t".join(shop_product_set)
        res_list = []
        flag = False
        for shop_range in all_range:
            # print shop_range

            ################
            product_count = 0
            for product_info in shop_product_set:
                if product_info.find(shop_range) != -1:
                    product_count += 1
            ###################
            # product_count = product_set_str.count(shop_range)
            if product_count > 0:
                flag = True
                res_list.append((shop_range, float(product_count) / product_all_count))
        if not flag:#如果商户范围没有大于0的商户
            continue
        res = [shop_id]
        # print shop_id+"\t",
        for range_rate in res_list:
            range_r = range_rate[0] + "_" + str(range_rate[1])
            res.append(range_r)
        fo.write("\t".join(res)+"\n")


def get_wid_dishes(shop_id_products):
    """
    获取商户id,和菜品
    :param shop_id_products:
    :return:
    """
    fo = open("/Users/Zealot/Desktop/waimai/all_shop_id_dishes.txt", "w")
    for shop_id_product_set in shop_id_products:
        shop_id = shop_id_product_set[0]
        shop_product_set = shop_id_product_set[1]
        product_all_count = len(shop_product_set)
        if product_all_count == 0:
            continue
        product_set_str = "\t".join(shop_product_set)
        fo.write(shop_id + "\t" + product_set_str+"\n")


def export_shop_id_dishes_file(file_path="shop_dishes_info.log"):
    """
    获取商户id，商户名称，菜品,导出到文件当中,用来计算第三步
    通过商户菜品的json文件中获取
    :return:
    """
    shop_id_products = []
    fo = open("/Users/Zealot/Desktop/waimai/shop_id_dishes.txt", "w")
    for line in open(file_path):
        shop_id = line.split(delimiter_blank)[0]
        shop_postfix = line.split(delimiter_blank)[1]
        products = []

        #所有的产品列表
        products = []
        decodeb = json.loads(shop_postfix)
        for categoryId_name in decodeb:
            # print categoryId_name, decodeb[categoryId_name]
            for product_id_name in decodeb[categoryId_name]:
                p_name = product_id_name.split("_")[1]
                products.append(p_name)

        shop_id_products.append((shop_id, products))
        fo.write(shop_id + "\t" + "\t".join(products) + "\n")


def main():
    all_range = get_all_range()
    # for range in all_range:
    #     print range
    shop_id_products = get_shop_id_name_dishes(shop_dishes_info_path)
    # export_shop_id_dishes_file(shop_dishes_info_path)
    get_range_by_dish_name(all_range, shop_id_products)
    # get_all_dishes(shop_dishes_info_path)
    # get_wid_dishes(shop_id_products)
    a={}


if __name__ == '__main__':
    main()