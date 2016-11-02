# -*- coding: utf-8 -*-

import os, sys, shutil
import datetime
import json
import re
import cPickle as ce
import sys_constant as sc
import __init__ as ini
reload(sys)
sys.setdefaultencoding('utf8')
# ############
# using for  check order up/down
# 处理订单，转换成需要的格式
#


class OnlineOrderProcess(object):
    """docstring for OnlineOrderPrecess"""

    def __init__(self, fpath_order, fpath_out):
        super(OnlineOrderProcess, self).__init__()
        self.fpath_order = fpath_order
        self.fpath_out = fpath_out
        self.order = {}

    def LoadOrder(self):
        with open(self.fpath_order, 'r') as fr:
            for line in fr:
                adid, ad_uid, mid, time_f, buy_type, buy_num, max_buy_num = line.strip().split()
                # time_f,o_flag,buy_num,buy_type = tmp_info.strip().split('|')
                if adid == '16081405019053000288':
                    print line
                if adid not in self.order.keys():
                    self.order[adid] = {'mid': mid}
                    self.order[adid]['ad_uid'] = ad_uid
                    self.order[adid]['fanstop_num'] = 0
                    self.order[adid]['feifen_num'] = 0
                    self.order[adid]['orientation_num'] = 0
                    self.order[adid]['feifen_maxnum'] = 0
                    self.order[adid]['buy_type'] = 0
                    self.order[adid]['bag_code'] = []
                    self.order[adid]['sel_uid'] = {}
                #指定账号
                if buy_type.startswith('u'):
                    self.order[adid]['sel_uid'][buy_type] = [buy_num, max_buy_num]
                #粉条
                elif buy_type == '-1':
                    self.order[adid]['buy_type'] = 0
                    self.order[adid]['fanstop_num'] = int(buy_num)
                #非粉
                elif buy_type == '0':
                    if self.order[adid]['buy_type'] == 2:
                        self.order[adid]['buy_type'] = 3
                    else:
                        self.order[adid]['buy_type'] = 1
                    self.order[adid]['feifen_num'] = int(buy_num)
                    if max_buy_num == 'NULL':
                        print line
                    else:
                        self.order[adid]['feifen_maxnum'] = int(max_buy_num)

                #定向包
                elif buy_type.startswith('20'):
                    if self.order[adid]['buy_type'] == 1:
                        self.order[adid]['buy_type'] = 3
                    else:
                        self.order[adid]['buy_type'] = 2
                    self.order[adid]['orientation_num'] += int(buy_num)
                    self.order[adid]['bag_code'].append([buy_type, buy_num])

    def load_order(self):
        with open(self.fpath_order, 'r') as fr:
            for line in fr:
                adid, ad_uid, mid, time_f, buy_type, buy_num, max_buy_num = line.strip().split()
                if adid not in self.order.keys():  # order中的adid初始化
                    self.order[adid] = {'mid': mid}
                    self.order[adid]['ad_uid'] = ad_uid
                    self.order[adid]['fanstop_num'] = 0
                    self.order[adid]['feifen_num'] = 0
                    self.order[adid]['orientation_num'] = 0
                    self.order[adid]['feifen_maxnum'] = 0
                    self.order[adid]['buy_type'] = 0
                    self.order[adid]['bag_code'] = []
                    self.order[adid]['sel_uid'] = {}
                    self.order[adid]['is_buy_fanstop'] = False
                    self.order[adid]['is_buy_feifen'] = False
                    self.order[adid]['is_buy_orientation'] = False
                    self.order[adid]['is_buy_sel_uid'] = False
                # 指定账号
                if buy_type.startswith(sc.adid_dataprod_buy_type_sel_uid):
                    self.order[adid]['sel_uid'][buy_type] = [buy_num, max_buy_num]
                    self.order[adid]['is_buy_sel_uid'] = True
                #粉条
                elif buy_type == sc.adid_dataprod_buy_type_fanstop:
                    self.order[adid]['fanstop_num'] = int(buy_num)
                    self.order[adid]['is_buy_fanstop'] = True
                #非粉
                elif buy_type == sc.adid_dataprod_buy_type_fei_fen:
                    self.order[adid]['feifen_num'] = int(buy_num)
                    self.order[adid]['is_buy_feifen'] = True
                    if max_buy_num == 'NULL':
                        print line
                    else:
                        self.order[adid]['feifen_maxnum'] = int(max_buy_num)
                #定向包
                elif buy_type.startswith(sc.adid_dataprod_buy_type_orientation):
                    self.order[adid]['orientation_num'] += int(buy_num)
                    self.order[adid]['bag_code'].append([buy_type, buy_num])
                    self.order[adid]['is_buy_orientation'] = True

    def cal_order_buy_type(self):
        """
        计算所有订单的购买类型
        :return:
        """
        with open(self.fpath_order, 'r') as fr:
            for line in fr:
                adid = line.strip().split()[0]
                if adid in self.order and self.order[adid]['buy_type'] == 0:  # 如果该广告id在order中，并且购买类型没有修改过，是0，则进行购买类型计算
                    is_buy_fanstop = self.order[adid]['is_buy_fanstop']
                    is_buy_feifen = self.order[adid]['is_buy_feifen']
                    is_buy_orientation = self.order[adid]['is_buy_orientation']
                    is_buy_sel_uid = self.order[adid]['is_buy_sel_uid']
                    buy_type = self.cal_buy_type(is_buy_fanstop, is_buy_feifen, is_buy_orientation, is_buy_sel_uid)
                    # print("buy_type:" + adid, str(buy_type), is_buy_fanstop, is_buy_feifen, is_buy_orientation, is_buy_sel_uid)
                    self.order[adid]['buy_type'] = buy_type

    def cal_buy_type(self, is_buy_fanstop, is_buy_feifen, is_buy_orientation, is_buy_sel_uid):
        """
        根据从原始数据源中获取的订单数据，计算购买类型。
        用来后边计算购买建议
        :param is_buy_fanstop:
        :param is_buy_feifen:
        :param is_buy_orientation:
        :param is_buy_sel_uid:
        :return:
        """
        buy_type = 1
        if is_buy_fanstop and not is_buy_feifen and not is_buy_orientation and not is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_fanstop
        elif not is_buy_fanstop and is_buy_feifen and not is_buy_orientation and not is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_feifen
        elif not is_buy_fanstop and not is_buy_feifen and is_buy_orientation and not is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_orientation
        elif not is_buy_fanstop and not is_buy_feifen and not is_buy_orientation and is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_sel_uid
        elif is_buy_fanstop and is_buy_feifen and is_buy_orientation and is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_fanstop_feifen_orientation_sel_uid
        elif is_buy_fanstop and is_buy_feifen and not is_buy_orientation and not is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_fanstop_feifen
        elif is_buy_fanstop and not is_buy_feifen and is_buy_orientation and not is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_fanstop_orientation
        elif is_buy_fanstop and not is_buy_feifen and not is_buy_orientation and is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_fanstop_sel_uid
        elif not is_buy_fanstop and is_buy_feifen and is_buy_orientation and not is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_feifen_orientation
        elif not is_buy_fanstop and is_buy_feifen and not is_buy_orientation and is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_feifen_sel_uid
        elif not is_buy_fanstop and not is_buy_feifen and is_buy_orientation and is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_orientation_sel_uid
        elif is_buy_fanstop and is_buy_feifen and is_buy_orientation and not is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_fanstop_feifen_orientation
        elif is_buy_fanstop and is_buy_feifen and not is_buy_orientation and is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_fanstop_feifen_sel_uid
        elif is_buy_fanstop and not is_buy_feifen and is_buy_orientation and is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_fanstop_orientation_sel_uid
        elif not is_buy_fanstop and is_buy_feifen and is_buy_orientation and is_buy_sel_uid:
            buy_type = sc.bowen_toutiao_feifen_orientation_sel_uid
        return buy_type

    def OrderData(self):

        # 读取即时订单
        # self.LoadOrder()
        self.load_order()

        #读取有效订单，合并到原来的订单里边，输出到order_data
        if os.path.exists('../data'):
            pass
        else:
            os.mkdir('../data')
        if os.path.exists('../data/order_record.pkl'):  #文件读写可能会出错，如果出错，使用备份文件order_record_back.pkl
            try:
                self.order_record = ce.load(open('../data/order_record.pkl', 'rb'))
                shutil.copyfile('../data/order_record.pkl', '../data/order_record_back.pkl')
            except:
                self.order_record = ce.load(open('../data/order_record_back.pkl', 'rb'))
        else:
            self.order_record = {}

        time_flag = str((datetime.datetime.now() + datetime.timedelta(hours=-20)))
        #合并即时订单与有效订单
        for adid in self.order.keys():
            if adid not in self.order_record.keys() and isinstance(adid, basestring):
                self.order_record[adid] = self.order[adid]
                self.order_record[adid]['time'] = str(datetime.datetime.now())
            elif len(self.order_record[adid]['bag_code']) < len(self.order[adid]['bag_code']) or self.order[adid][
                'feifen_num'] > self.order_record[adid]['feifen_num']:
                if adid == '16081405019053000288':
                    print "YES modify"
                self.order_record[adid] = self.order[adid]
                self.order_record[adid]['time'] = str(datetime.datetime.now())
        for adid in self.order_record.keys():  #检查订单是否超时（投放超过24小时，删掉）
            if self.order_record[adid]['time'] < time_flag:
                del self.order_record[adid]

        #输出当前有效订单
        with open(self.fpath_out, 'w') as fw:
            for (adid, v) in self.order_record.items():
                fw.write(adid + '\t' + json.dumps(v) + '\n')
        ce.dump(self.order_record, open('../data/order_record.pkl', 'wb'))

        return self.order_record

    def order_data(self):
        """
        读取即时订单,把线上的同步到目前的
        :return:
        """
        # 读取即时订单
        self.load_order()
        #计算购买类型
        self.cal_order_buy_type()
        # 把线上的同步到目前的
        self.combine_data_from_order_to_record()

        return self.order_record

    def combine_data_from_order_to_record(self):
        #读取有效订单，合并到原来的订单里边，输出到order_data
        if os.path.exists('../data'):
            pass
        else:
            os.mkdir('../data')
        if os.path.exists('../data/order_record.pkl'):  #文件读写可能会出错，如果出错，使用备份文件order_record_back.pkl
            try:
                self.order_record = ce.load(open('../data/order_record.pkl', 'rb'))
                shutil.copyfile('../data/order_record.pkl', '../data/order_record_back.pkl')
            except:
                self.order_record = ce.load(open('../data/order_record_back.pkl', 'rb'))
        else:
            self.order_record = {}

        time_flag = str((datetime.datetime.now() + datetime.timedelta(hours=-20)))
        #合并即时订单与有效订单
        for adid in self.order.keys():
            if adid not in self.order_record.keys() and isinstance(adid, basestring):
                self.order_record[adid] = self.order[adid]
                self.order_record[adid]['time'] = str(datetime.datetime.now())
            elif len(self.order_record[adid]['bag_code']) < len(self.order[adid]['bag_code']) or \
                            self.order[adid]['feifen_num'] > self.order_record[adid]['feifen_num'] or \
                            len(self.order[adid]['sel_uid']) > len(self.order_record[adid]['sel_uid']) or \
                            self.order[adid]['fanstop_num'] > self.order_record[adid]['fanstop_num']:
                if adid == '16081405019053000288':
                    print "YES modify"
                self.order_record[adid] = self.order[adid]
                self.order_record[adid]['time'] = str(datetime.datetime.now())
        for adid in self.order_record.keys():  #检查订单是否超时（投放超过24小时，删掉）
            if self.order_record[adid]['time'] < time_flag:
                del self.order_record[adid]

        #输出当前有效订单
        with open(self.fpath_out, 'w') as fw:
            for (adid, v) in self.order_record.items():
                fw.write(adid + '\t' + json.dumps(v) + '\n')
        ce.dump(self.order_record, open('../data/order_record.pkl', 'wb'))

    def LoadData(self):
        # data 测试订单数据
        order_data = ce.load(open('../data/order_record.pkl', 'rb'))
        i = 0
        with open('./test.txt', 'r') as fr:
            for line in fr:
                print 'line:', line
                adid, val = line.strip().split('\t')
                values = json.loads(val)
                print adid + '\t', order_data[adid]['mid']
                print adid + '\t', order_data[adid]['ad_uid']
                print adid + '\t', order_data[adid]['time']
                print adid + '\t', order_data[adid]['buy_type']
                print adid + '\t', order_data[adid]['feifen_num']
                print adid + '\t', order_data[adid]['fanstop_num']
                print adid + '\t', order_data[adid]['orientation_num']
                print adid + '\t', order_data[adid]['bag_code']
                print adid + '\t', order_data[adid]['sel_uid']
                print "-----------------------------------"
                i += 1
                if i == 10:
                    break


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "parameters ERRO: <adid_path><fpath_out>"
        sys.exit(1)
    myOnlineOrder = OnlineOrderProcess(sys.argv[1], sys.argv[2])
    ini.logger.warning("begin...")
    ini.logger.info("begin...")
    # order_data = myOnlineOrder.OrderData()
    order_data_latest = myOnlineOrder.order_data()
    ini.logger.info(len(order_data_latest))
#myOnlineOrder.LoadData()
