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
range_shop_name_mapping_path = "/Users/Zealot/Desktop/waimai/fu_zhu_ci_biao"
# range_shop_name_mapping_path = "/Users/Zealot/Desktop/waimai/shop_range_mapping_17"
#所有商户id，菜品名称
shop_dishes_info_path = "/Users/Zealot/Desktop/waimai/widDishTag.log"
#北京商户id，名称
# shop_dishes_info_path = "/Users/Zealot/Desktop/waimai/beijing_wids"

output = "/Users/Zealot/Desktop/waimai/1010_2.txt"

#所有的经营范围

delimiter_blank = "\t"


def get_all_range():
    """
    获取所有的经营范围
    :return:
    """
    all_range = []
    # #{辅助词：经营范围}
    # all_range_map = {}
    # for line in open(range_shop_name_mapping_path):
    #     fields = line.strip().split("\t")
    #     all_range.append(fields[0])
    #     range_name = fields[0]
    #     for index in fields[:]:
    #         if index.strip() != "" and index != "\t":
    #             all_range_map[index] = range_name
    #{经营范围，辅助词列表}
    all_range_fuzhuci_map = {}
    for line in open(range_shop_name_mapping_path):
        fields = line.strip().split("\t")
        range_name = fields[0]
        all_range.append(range_name)
        fuzhuci_list = []
        for index in fields[:]:
            if index.strip() != "" and index != "\t":
                fuzhuci_list.append(index)
        all_range_fuzhuci_map[range_name] = fuzhuci_list

    return all_range_fuzhuci_map


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


def get_range_by_dish_name(shop_id_products, all_range_map):
    fo = open(output, "w")
    for shop_id_product_set in shop_id_products:
        shop_id = shop_id_product_set[0]
        shop_product_set = shop_id_product_set[1]
        product_all_count = len(shop_product_set)
        if product_all_count == 0:
            continue
        res_list = []
        flag = False
        for fu_zhu_ci in all_range_map.keys():
            product_count = 0
            for cai_pin_name in shop_product_set:
                if cai_pin_name.find(fu_zhu_ci) != -1:
                    product_count += 1
            if product_count > 0:
                flag = True
                res_list.append((all_range_map[fu_zhu_ci], float(product_count) / product_all_count))
        if not flag:#如果商户范围没有大于0的商户
            continue
        res = [shop_id]
        # print shop_id+"\t",
        for range_rate in res_list:
            range_r = range_rate[0] + "_" + str(range_rate[1])
            res.append(range_r)
        fo.write("\t".join(res)+"\n")


def get_range_by_dish_name2(shop_id_products, all_range_fuzhuci_map):
    fo = open(output, "w")
    for shop_id_product_set in shop_id_products:
        shop_id = shop_id_product_set[0]
        shop_product_set = shop_id_product_set[1]
        product_all_count = len(shop_product_set)
        if product_all_count == 0:
            continue
        res_map = {}#{经营范围，数量}
        flag = False
        for cai_pin_name in shop_product_set:#商户中的菜品集中，选出一个
            for shop_range in all_range_fuzhuci_map.keys():#遍历所有经营范围
                fuzhuci_list = all_range_fuzhuci_map[shop_range]#获取所有的辅助词
                for fu_zhu_ci in fuzhuci_list:#只要有一个辅助词匹配到了，则此经营范围的数量+1,并跳出循环
                    if cai_pin_name.find(fu_zhu_ci) != -1:
                        flag = True
                        # print "辅助词："+fu_zhu_c
                        # print "a:"+res_map.has_key(shop_range)i
                        # print "a:"+res_map.has_key(shop_range)
                        if shop_range in res_map.keys():
                            range_count = res_map[shop_range]
                            res_map[shop_range] = range_count + 1
                        else:
                            res_map[shop_range] = 1
                        break

        if not flag:#如果商户范围没有大于0的商户
            continue
        res = [shop_id]
        for range_name, count in res_map.items():
            range_r = range_name + "_" + str(float(count)/product_all_count)
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
    all_range_fuzhuci_map = get_all_range()
    # for range in all_range_fuzhuci_map:
    #     print range
    shop_id_products = get_shop_id_name_dishes(shop_dishes_info_path)
    get_range_by_dish_name2(shop_id_products, all_range_fuzhuci_map)
    # export_shop_id_dishes_file(shop_dishes_info_path)

    # get_all_dishes(shop_dishes_info_path)
    # get_wid_dishes(shop_id_products)

if __name__ == '__main__':
    main()