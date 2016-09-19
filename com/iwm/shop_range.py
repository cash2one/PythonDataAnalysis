#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Zealot'

# import MySQLdb
import json

''''
商户转换成经营范围。一个商户会有多个标签，每个标签会对应一个权重。
1、通过商户id，找到商户名称，匹配到经营范围。
2、通过菜品名称，匹配到经营范围。
'''

delimiter_blank = "\t"
# SQL 查询语句
sql = "SELECT * FROM EMPLOYEE WHERE id = ?1"
# 打开数据库连接
# db = MySQLdb.connect("localhost", "testuser", "test123", "TESTDB")


def get_shop_ids(file_path="shop_dishes_info.log"):
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


# def get_shop_name_by_id(shop_id):
#     """
#     通过sql查到每一个的商户名称。
#     :param shop_id:
#     :return:
#     """
#     name = ""
#     # 使用cursor()方法获取操作游标
#     cursor = db.cursor()
#     sql2 = sql.replace("?1", shop_id)
#     try:
#         # 执行SQL语句
#         cursor.execute(sql2)
#         # 获取所有记录列表
#         results = cursor.fetchall()
#         for row in results:
#             name = row[0]
#             # 打印结果
#             #print "fname=%s,lname=%s,age=%d,sex=%s,income=%d" % (fname, lname, age, sex, income )
#     except:
#         print "Error: unable to fecth data"
#     return name


# def get_shop_id_name(shop_ids):
#     shop_id_name = []
#     for shop_id in shop_ids:
#         shop_name = get_shop_name_by_id(shop_id)
#         shop_id_name.append((shop_id, shop_name))
#     return shop_id_name


def get_shop_id_product(file_path="shop_dishes_info.log"):
    """
    读取文件
    :return:得到每一个商户id，产品名称
    """
    shop_id_products = []
    for line in open(file_path):
        shop_id = line.split(delimiter_blank)[0]
        shop_postfix = line.split(delimiter_blank)[1]
        products = []

        #所有的产品列表
        products = []
        products_set = set(products)
        index = 0
        # encodedb = json.dumps(shop_postfix)
        decodeb = json.loads(shop_postfix)
        index = 0
        for categoryId_name in decodeb:
            # print categoryId_name, decodeb[categoryId_name]
            for product_id_name in decodeb[categoryId_name]:
                #p_id = product_id_name.split("_")[0]
                print categoryId_name
                p_name = product_id_name.split("_")[1]
                print p_name
                #products.append(p_name)
                products_set.add(p_name)

        shop_id_products.append((shop_id, products_set))
        #print shop_id,
    return shop_id_products


def main():
    #shop_ids = get_shop_ids()
    #print shop_ids
    #shop_id_name = get_shop_id_name(shop_ids)
    #TODO 通过商户名字，匹配经营范围
    shop_id_products = get_shop_id_product()
    #TODO 通过商户出品的产品的名字，匹配经营范围

if __name__ == '__main__':
    main()