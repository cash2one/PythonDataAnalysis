# -*- coding:utf-8 -*-
import cPickle as ce
import os
import sys
import datetime


def ctr_week_avg(dir_path):
    ctr_data = {}
    history_order = ce.load(open(dir_path + '/data/history_order_data.pkl', 'rb'))
    #history_order_back = ce.load(open('../data/history_order_record_back.pkl','rb'))
    time_60 = str(datetime.datetime.now() + datetime.timedelta(days=-60))
    time_8 = str(datetime.datetime.now() + datetime.timedelta(days=-10))
    tmp_static = {'0fanstop_num': 0, '0fanstop_interact': 0.0, '1fanstop_num': 0, '1fanstop_interact': 0.0,
                  '0feifen_num': 0, \
                  '0feifen_interact': 0.0, '1feifen_num': 0, '1feifen_interact': 0.0, '0orientation_num': 0,
                  '0orientation_interact': 0.0, '1orientation_num': 0, '1orientation_interact': 0.0}
    item_list = ['fanstop', 'feifen', 'orientation']
    expo_flag = '_expo'
    expo_num = 1
    sta_ctr = {}
    recmd_num = 0
    sta_num = {'0_fanstop_num': 0, '1_fanstop_num': 0, '0_feifen_num': 0, '1_feifen_num': 0, '0_orientation_num': 0,
               '1_orientation_num': 0}
    for (adid, values) in history_order.items():
        if adid.endswith('week') or values['time'] < time_8:
            continue
        #history_order_back[adid] = values
        for way in item_list:
            if "video_flag" not in values.keys():
                print adid, values
                continue
            if way + expo_flag not in values.keys():
                expo_num += 1
            #print adid,values
            #print values["video_flag"],values[way+'_ctr']
            tmp_static[str(values["video_flag"]) + way + '_interact'] += float(values[way + '_ctr']) * values[
                way + expo_flag]
            tmp_static[str(values["video_flag"]) + way + '_num'] += values[way + expo_flag]
            if values[way + '_num'] != 0:
                if str(values["video_flag"]) + '_' + way + '_ctr' in sta_ctr.keys():
                    if str(values[way + '_ctr']) in sta_ctr[str(values["video_flag"]) + '_' + way + '_ctr'].keys():
                        sta_ctr[str(values["video_flag"]) + '_' + way + '_ctr'][str(values[way + '_ctr'])] += 1
                    else:
                        sta_ctr[str(values["video_flag"]) + '_' + way + '_ctr'][str(values[way + '_ctr'])] = 1
                else:
                    sta_ctr[str(values["video_flag"]) + '_' + way + '_ctr'] = {str(values[way + '_ctr']): 1}
                sta_num[str(values["video_flag"]) + '_' + way + '_num'] += 1
    for way in item_list:
        ctr_data['0_' + way + '_ctr_week'] = float(tmp_static['0' + way + '_interact']) / tmp_static[
            '0' + way + '_num'] if tmp_static['0' + way + '_num'] != 0 else 0
        ctr_data['1_' + way + '_ctr_week'] = float(tmp_static['1' + way + '_interact']) / tmp_static[
            '1' + way + '_num'] if tmp_static['1' + way + '_num'] != 0 else 0
        print '0_' + way + '_ctr_week:', tmp_static['0' + way + '_interact'], tmp_static['0' + way + '_num'], ctr_data[
            '0_' + way + '_ctr_week']
        print '1_' + way + '_ctr_week:', tmp_static['1' + way + '_interact'], tmp_static['1' + way + '_num'], ctr_data[
            '1_' + way + '_ctr_week']
    print 'tmp_static:', tmp_static
    print 'ctr_data:', ctr_data
    print 'sta_num:', sta_num
    print 'recmd_num:', recmd_num
    print "no expo key num:", expo_num
    ctr_week_out = {}
    for (k, v) in sta_ctr.items():
        split_num = 0
        tmp_tuple = sorted(v.items(), key=lambda d: d[0], reverse=True)
        #if '0fanstop' in k:
        #	print k,tmp_tuple
        valid_num = float(sta_num[k[:-3] + 'num']) * 0.75
        if float(tmp_tuple[len(tmp_tuple) - 1][1]) / int(sta_num[k[:-3] + 'num']) > 0.5:
            valid_num = (float(sta_num[k[:-3] + 'num']) - float(tmp_tuple[len(tmp_tuple) - 1][1])) * 0.95
        elif float(tmp_tuple[len(tmp_tuple) - 1][1]) / int(sta_num[k[:-3] + 'num']) > 0.4:
            valid_num = (float(sta_num[k[:-3] + 'num']) - float(tmp_tuple[len(tmp_tuple) - 1][1])) * 0.93
        elif float(tmp_tuple[len(tmp_tuple) - 1][1]) / int(sta_num[k[:-3] + 'num']) > 0.3:
            valid_num = (float(sta_num[k[:-3] + 'num']) - float(tmp_tuple[len(tmp_tuple) - 1][1])) * 0.92
        elif float(tmp_tuple[len(tmp_tuple) - 1][1]) / int(sta_num[k[:-3] + 'num']) > 0.2:
            valid_num = (float(sta_num[k[:-3] + 'num']) - float(tmp_tuple[len(tmp_tuple) - 1][1])) * 0.91
        elif float(tmp_tuple[len(tmp_tuple) - 1][1]) / int(sta_num[k[:-3] + 'num']) > 0.15:
            valid_num = (float(sta_num[k[:-3] + 'num']) - float(tmp_tuple[len(tmp_tuple) - 1][1])) * 0.9
        for i in range(len(tmp_tuple)):
            if split_num > valid_num:
                print split_num, int(sta_num[k[:-3] + 'num']) * 0.75
                ctr_week_out[k + '_week'] = tmp_tuple[i][0]
                break
            split_num += int(tmp_tuple[i][1])
        print split_num, int(sta_num[k[:-3] + 'num']) * 0.75
    history_ctr_week = {}
    update_flag = 1
    with open(dir_path + '/data/ctr_week_avg.txt', 'r') as fr:
        for line in fr:
            take = line.strip().split('\t')
            if 'mid' in take[0]:
                continue
            history_ctr_week[take[0]] = float(take[1])
            if float(ctr_week_out[take[0]]) / float(take[1]) > 1.25 or float(ctr_week_out[take[0]]) / float(
                    take[1]) < 0.75:
                update_flag = 0
    if 1 == update_flag:
        with open(dir_path + '/data/ctr_week_avg_update.txt', 'w') as fw:
            for (k, v) in ctr_week_out.items():
                fw.write(k + '\t' + str(v) + '\n')
            fw.write('mid_rpm_week' + '\t' + '0.0004' + '\n')
    print "ctr_week_out:", ctr_week_out

    fw = open("../data/out_data/history_ctr_stactic.txt", 'w')
    for (k1, v1) in sta_ctr.items():
        for (k2, v2) in v1.items():
            fw.write(k1 + "\t" + k2 + "\t" + str(v2) + "\n")
        #ce.dump(history_order,open('../data/history_order_record_check.pkl','wb'))


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print "parameters erro:<file dir_path>"
    ctr_week_avg(sys.argv[1])
