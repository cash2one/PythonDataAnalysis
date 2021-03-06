# -*- coding: utf-8 -*-
import os, shutil
import cPickle as ce
import json
import redis
import sys
import utils as util
from upfans_suggestion import *
from bowen_suggestion import *
from recmd_bags import *
from buy_option_suggestion import *

reload(sys)
sys.setdefaultencoding('utf8')


def HistoryOrderDataSel(dir_path, history_order_data):
    time_7 = str((datetime.datetime.now() + datetime.timedelta(hours=-168)))
    for adid in history_order_data.keys():
        if adid.endswith('week'):
            continue
        if history_order_data[adid]['time'] < time_7:
            del history_order_data[adid]
    ce.dump(history_order_data, open(dir_path + "/data/history_order_data.pkl", 'wb'))
    return history_order_data


def LoadOrder(dir_path):
    #print dir_path
    if os.path.isfile(dir_path + "/data/order_data.pkl"):
        #order_data = ce.load(open(dir_path+"/data/order_data.pkl"))
        #shutil.copyfile(dir_path+"/data/order_data.pkl",dir_path+"/data/order_data_back.pkl")
        try:
            order_data = ce.load(open(dir_path + "/data/order_data.pkl"))
            shutil.copyfile(dir_path + "/data/order_data.pkl", dir_path + "/data/order_data_back.pkl")
        except:
            order_data = ce.load(open(dir_path + "/data/order_data_back.pkl"))
    else:
        order_data = {}
    time_flag = str((datetime.datetime.now() + datetime.timedelta(hours=-72)))
    with open(dir_path + "/data/order_data.txt", 'r') as fr:
        for line in fr:
            try:
                adid, v_t = line.strip().split('\t')
            except:
                print line
                sys.exit(1)
            if adid in order_data.keys():
                continue
            try:
                values = json.loads(v_t)
            except:
                print v_t
                continue

            order_data[adid] = values
            order_data[adid]['time'] = str(datetime.datetime.now())
    print "order_data:", len(order_data)
    if os.path.exists(dir_path + "/data/history_order_data.pkl"):
        try:
            history_order_data = ce.load(open(dir_path + "/data/history_order_data.pkl", 'rb'))
            shutil.copyfile(dir_path + "/data/history_order_data.pkl", dir_path + "/data/history_order_data_back.pkl")
        except:
            history_order_data = ce.load(open(dir_path + "/data/history_order_data_back.pkl", 'rb'))
    else:
        history_order_data = {}
    with open(dir_path + "/data/ctr_week_avg.txt", 'r') as fr:
        for line in fr:
            take = line.strip().split()
            history_order_data[take[0]] = float(take[1])
    order_data['0_fanstop_ctr_week'] = history_order_data['0_fanstop_ctr_week']
    order_data['1_fanstop_ctr_week'] = history_order_data['1_fanstop_ctr_week']
    order_data['0_feifen_ctr_week'] = history_order_data['0_feifen_ctr_week']
    order_data['1_feifen_ctr_week'] = history_order_data['1_feifen_ctr_week']
    order_data['0_orientation_ctr_week'] = history_order_data['0_orientation_ctr_week']
    order_data['1_orientation_ctr_week'] = history_order_data['1_orientation_ctr_week']
    order_data['mid_rpm_week'] = history_order_data['mid_rpm_week']
    if '1_sel_uid_ctr_week' in history_order_data:
        order_data['1_sel_uid_ctr_week'] = history_order_data['1_sel_uid_ctr_week']
    else:
        order_data['1_sel_uid_ctr_week'] = 0.01
    if '0_sel_uid_ctr_week' in history_order_data:
        order_data['0_sel_uid_ctr_week'] = history_order_data['0_sel_uid_ctr_week']
    else:
        order_data['0_sel_uid_ctr_week'] = 0.001
    return order_data, history_order_data


def InteractData(order_data):#获取互动，曝光
    inter_data = {}
    r = redis.Redis(host='rs20468.hebe.grid.sina.com.cn', port=20468)
    #10.75.29.90:5861
    r_back = redis.Redis(host='rm20468.eos.grid.sina.com.cn', port=20468)
    for (adid, value) in order_data.items():
        if adid.endswith('week'):
            continue
        try:
            try:
                inter_data[adid] = [r.hgetall(adid + '_interact_advice_nums'), r.hgetall(adid + '_expo_user_profile')]
            except Exception:
                inter_data[adid] = [r_back.hgetall(adid + '_interact_advice_nums'),
                                    r_back.hgetall(adid + '_expo_user_profile')]
            # ini.logger.info(inter_data[adid])
        except Exception:
            raise RuntimeError("InteractData Error")
    print len(inter_data)
    return inter_data


def CtrData(order_data, bowen_result, inter_data, history_order_data):
    #return ctr and video flag
    #tran:14000003 , cmt:14000005 url:14000014 col:14000045 zan:14000098 video:25000003 80000001 pic:50000004 #remove 50000004
    inter_code = ['14000003', '14000005', '14000014', '14000045', '14000098', '25000003', '80000001', '14000008']#转、赞
    adid_mod_num = 100
    for (adid, value) in order_data.items():
        if adid.endswith('week'):
            continue
        adid_mod = int(adid) % adid_mod_num
        order_data[adid]['orientation_ctr'] = 0.0
        order_data[adid]['feifen_ctr'] = 0.0
        order_data[adid]['fanstop_ctr'] = 0.0
        order_data[adid]["feifen_expo"] = 0
        order_data[adid]["fanstop_expo"] = 0
        order_data[adid]["orientation_expo"] = 0
        order_data[adid]['video_flag'] = 0
        order_data[adid]['sel_uid_ctr'] = 0.0
        order_data[adid]["sel_uid_expo"] = 0

        if adid in inter_data.keys():
            for itm in inter_data[adid][0].keys():
                if '25000003' in itm or '80000001' in itm:
                    if int(inter_data[adid][0][itm]) > 0:
                        #pass
                        order_data[adid]['video_flag'] = 1
        if adid in inter_data.keys():
            if adid.endswith('expo'):
                continue
            #print adid,order_data[adid]
            if order_data[adid]['feifen_num'] != 0:
                ctr_num = 0
                for act_code in inter_code:
                    if 'nofans_' + act_code in inter_data[adid][0].keys():#非粉
                        ctr_num += int(inter_data[adid][0]['nofans_' + act_code])
                if "extendfans" in inter_data[adid][1].keys():
                    order_data[adid]["feifen_expo"] = int(inter_data[adid][1]["extendfans"])
                    order_data[adid]['feifen_ctr'] = float(ctr_num) / int(inter_data[adid][1]["extendfans"]) if int(
                        inter_data[adid][1]["extendfans"]) != 0 else 0
            if order_data[adid]['orientation_num'] != 0:
                ctr_num = 0
                for act_code in inter_code:
                    if 'fields_' + act_code in inter_data[adid][0].keys():
                        ctr_num += int(inter_data[adid][0]['fields_' + act_code])
                if "fieldfans" in inter_data[adid][1].keys():
                    order_data[adid]["orientation_expo"] = int(inter_data[adid][1]['fieldfans'])
                    order_data[adid]['orientation_ctr'] = float(ctr_num) / int(inter_data[adid][1]['fieldfans']) if int(
                        inter_data[adid][1]['fieldfans']) != 0 else 0
            if order_data[adid]['fanstop_num'] != 0:
                ctr_num = 0
                #print inter_data[adid]
                for act_code in inter_code:
                    if 'fanstop_' + act_code in inter_data[adid][0].keys():
                        ctr_num += int(inter_data[adid][0]['fanstop_' + act_code])
                if "fanstop" in inter_data[adid][1].keys():
                    order_data[adid]["fanstop_expo"] = int(inter_data[adid][1]['fanstop'])
                    order_data[adid]['fanstop_ctr'] = float(ctr_num) / int(inter_data[adid][1]['fanstop']) if int(
                        inter_data[adid][1]['fanstop']) != 0 else 0
            if order_data[adid]['sel_uid']:#sel_uid为order_data中的名字，字典数据。
                """
                新加指定账号数据
                """
                ctr_num = 0
                for act_code in inter_code:
                    if 'desdfans_' + act_code in inter_data[adid][0].keys():
                        ctr_num += int(inter_data[adid][0]['desdfans_' + act_code])
                if "desdfans" in inter_data[adid][1].keys():
                    order_data[adid]["sel_uid_expo"] = int(inter_data[adid][1]['desdfans'])
                    order_data[adid]['sel_uid_ctr'] = float(ctr_num) / int(inter_data[adid][1]['desdfans']) if int(
                        inter_data[adid][1]['desdfans']) != 0 else 0
            # ini.logger.info(order_data[adid])

        order_data[adid]['bowen_test_flag'] = 0
        if order_data[adid]['video_flag'] == 1:
            order_data[adid]['bowen_test_flag'] = 1
            order_data[adid]['video_flag'] == 1
        elif adid_mod in bowen_result.keys() and adid in bowen_result[adid_mod].keys():
            order_data[adid]['video_flag'] = int(bowen_result[adid_mod][adid][1])
            if int(bowen_result[adid_mod][adid][0]) == 1 or int(bowen_result[adid_mod][adid][1]) == 1:
                order_data[adid]['bowen_test_flag'] = 1
    time_flag = str((datetime.datetime.now() + datetime.timedelta(hours=-72)))
    #save no update data
    for adid in order_data.keys():
        if adid.endswith('week'):
            continue
        if order_data[adid]['time'] < time_flag:#如果订单下线，则删掉
            history_order_data[adid] = order_data[adid]
            del order_data[adid]
    return order_data, history_order_data


def OutData(output_path, order_data, bowen_result, upfans_result, buy_result):
    update_data = {}
    adid_mod_num = 100
    fw_test = open(output_path + "_check", 'w')
    with open(output_path, 'w') as fw:
        for (adid, v) in order_data.items():
            if adid.endswith('week'):
                continue
            tmp_result = {}
            adid_mod = int(adid) % adid_mod_num
            fw_test.write(adid + '\t')
            tmp_result['orientationFlag'] = 0
            tmp_result['version'] = 1
            fw_test.write('version:' + str(1) + '\t')
            tmp_result['orientationVol'] = []
            tmp_result['feifenVol'] = v['feifen_num'] if v['feifen_num'] != 0 else 0
            fw_test.write('feifenVol:' + str(tmp_result['feifenVol']) + '\t')
            tmp_result['suggestion'] = {}
            if order_data[adid]['bowen_test_flag'] == 0:
                tmp_result['suggestion']['bowen'] = u'博文中添加精美图片或视频可以有效提升推广效果哦!'
                fw_test.write('bowen:' + tmp_result['suggestion']['bowen'] + '\t')
            if adid in buy_result[adid_mod].keys():
                tmp_result['effect'] = buy_result[adid_mod][adid][0]
                tmp_result['suggestion']['fentiao'] = buy_result[adid_mod][adid][1]
                fw_test.write('fentiao:' + tmp_result['suggestion']['fentiao'] + '\t' + 'effect:' + str(
                    tmp_result['effect']) + '\t')
                if len(buy_result[adid_mod][adid]) > 2 and buy_result[adid_mod][adid][2] > 0:
                    tmp_result['orientationFlag'] = buy_result[adid_mod][adid][3]
                    for itm in buy_result[adid_mod][adid][2]:
                        tmp_result['orientationVol'].append({'code': itm[0], 'vol': int(itm[1])})
            else:
                print adid
            if adid in upfans_result[adid_mod].keys():
                if '1' == upfans_result[adid_mod][adid]:
                    tmp_result['suggestion']['fansmore'] = u'寻找活跃粉丝，扩大微博曝光，试试涨粉利器——账号头条吧!'
                    fw_test.write('fansmore:' + tmp_result['suggestion']['fansmore'] + '\t')
                elif '2' == upfans_result[adid_mod][adid]:
                    tmp_result['suggestion']['fansmore'] = u'寻找活跃粉丝，扩大微博曝光，试试涨粉利器——账号头条吧!'
                    fw_test.write('fansmore:' + tmp_result['suggestion']['fansmore'] + '\t')
            fw.write(adid + '\t' + json.dumps(tmp_result) + '\n')
            fw_test.write('orientationVol:' + json.dumps(tmp_result['orientationVol']) + '\t')
            fw_test.write('orientationFlag:' + str(tmp_result['orientationFlag']) + "\n")
            update_data[adid] = tmp_result
        #print json.dumps(tmp_result)
    return update_data


def combine_data(fpath_1, fpath_2, update_data):
    update_data_set = set(update_data.keys())
    with open(fpath_1, 'a') as fw:
        with open(fpath_2, 'r') as fr:
            for line in fr:
                take = line.strip().split()
                if take[0] not in update_data_set:
                    fw.write(line)


def main(dir_path):
    util.logger.info(dir_path + "/data/order_data.pkl")
    order_data, history_order_data = LoadOrder(dir_path)#！！！计算指定账号的7天平均CTR
    util.logger.info(["load data finsh: order_data num is ", len(order_data), "history_order_data num is ", len(history_order_data)])

    inter_data = InteractData(order_data)#获取互动数据
    util.logger.info([" inter_data finsh: inter_data num is ", len(inter_data)])

    #the dir_path use for storage mid content
    myBoWen = BowenSuggestion(dir_path, order_data)
    bowen_result = myBoWen.order_data_process()#博文质量检测
    util.logger.info([" bowen process finish: bowen_result num is ", len(bowen_result)])

    order_data, history_order_data = CtrData(order_data, bowen_result, inter_data, history_order_data)#72小时CTR!!!
    ce.dump(order_data, open(dir_path + '/data/order_data.pkl', 'wb'))
    util.logger.info([" ctr caculate finish: CtrData order_data num is ", len(order_data), "CtrData history_order_data num is ", len(history_order_data)])

    #split_words:mid_content
    #该部分若没有分词，则先将订单中的博文进行词后防置在 data文件夹下，名字为online_words.txt
    #格式所有词空格间隔，词:权重，3997213585840580:184 免费:115 唱:125 垃:圾:154 赚:133 报名:129 买不起:215 黑心:178 票:148 场外:145 祝:102 生日快乐:141 薛之谦:194 薛之谦:194 全球:152 后援会:179
    str1 = "/data0/chenwei9/fanstop_data_suggestion/weiboseg/WeiboSegmentor-v2.3.4-el5.4-64bit-lib-20130304"
    try:
        os.system(
            str1 + "/example/TokenizerExampleCpp " + str1 + "/conf/tokenizer.conf -e utf-8 -g both -w -f " + dir_path + "/data/mid_content.txt >" + dir_path + "/data/online_words.txt")
    except:
        print "words_seg erro,please input words by manu"

    util.logger.info("finish words segment")
    myBagProb = BagProb(dir_path, order_data) #定向包预测
    bags_recmd_result = myBagProb.Bag_Recmd()
    util.logger.info(["BagProb finish: bags_recmd_result num is ", len(bags_recmd_result)])

    myupfans = Upfans_Suggestion(dir_path, order_data)
    upfans_result = myupfans.suggestion_result() #涨粉建议
    util.logger.info(["upfans suggestion finish: upfans_result num is ", len(upfans_result)])

    mybuy_result = Buy_Option(dir_path, order_data, bags_recmd_result, bowen_result)#购买建议！！！！
    buy_result = mybuy_result.buy_suggestion()
    # print datetime.datetime.now(), " buy option finish: buy_result num is ", sum([len(i) for i in buy_result.values()])
    util.logger.info([" buy option finish: buy_result num is ", sum([len(i) for i in buy_result.values()])])
    if os.path.isdir(dir_path + "/data/out_data/"):
        pass
    else:
        os.mkdir(dir_path + "/data/out_data/")
    output_path = dir_path + '/data/out_data/update_data'#当次计算结果
    update_data = OutData(output_path, order_data, bowen_result, upfans_result, buy_result)
    util.logger.info("out data finish")
    #new_data use for select order  stop update  combine to old data
    new_data_path = dir_path + '/data/out_data/new_data'#上次（半小时前）的计算结果
    if os.path.isfile(dir_path + "/data/out_data/new_data"):
        pass
    else:
        os.mknod(dir_path + "/data/out_data/new_data")
    if os.path.isfile(dir_path + "/data/out_data/no_update_data"):#不再更新，已经计算完成（已经退出的、投放完成、超过24小时的订单）
        pass
    else:
        os.mknod(dir_path + "/data/out_data/no_update_data")
    no_update_data_path = dir_path + '/data/out_data/no_update_data'
    if os.path.isfile(new_data_path) and os.path.isfile(no_update_data_path):
        combine_data(no_update_data_path, new_data_path, update_data)
    history_order_data = HistoryOrderDataSel(dir_path, history_order_data)
    util.logger.info("finish all")


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print "please input dir path"
        sys.exit(1)
    main(sys.argv[1])
