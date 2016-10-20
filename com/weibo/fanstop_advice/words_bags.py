# -*- coding:utf-8 -*- 
import sys
import re
import cPickle
import codecs
import os


def WordsProcess(fpath):
    order_num = 0
    if os.path.exists('../data/word_bags.pkl'):
        words_bags = cPickle.load(open('../data/word_bags.pkl', 'rb'))
    else:
        words_bags = {}
    with codecs.open(fpath, 'r') as fr:
        for line in fr:
            # line format:mid bag_code words
            take = line.strip().split(' ')
            bag = take[2].split(':')[0]
            for itm in take[2:]:
                tk = itm.split(':')
                if tk[1] == '0' or re.search('.*([0-9a-zA-Z]+).*', tk[0]):
                    continue
                if tk[0] in words_bags.keys():
                    words_bags[tk[0]]['num'] += 1
                    if take[1] in words_bags[tk[0]].keys():
                        words_bags[tk[0]][bag] += 1
                    else:
                        words_bags[tk[0]][bag] = 1
                else:
                    words_bags[tk[0]] = {bag: 1}
                    words_bags[tk[0]]['num'] = 1
            order_num += 1
        words_bags['order_num'] += order_num
    cPickle.dump(words_bags, open('../data/word_bags.pkl', 'wb'))
    with open('../data/check_words_bags.txt', 'w') as fw:
        for (k, v) in words_bags.items():
            fw.write(k + '\t' + str(v) + '\n')
    print "finish WordsProcess"


def Bag_level(inter, pv):
    low_ratio = 0.0011
    high_ratio = 0.006
    ctr = float(inter) / float(pv)
    if ctr < low_ratio:
        return '0'
    elif ctr < high_ratio:
        return '1'
    else:
        return '2'


def BagProcess(fpath):
    ctr_set = set()
    if os.path.exists('../data/bags_ctr.pkl'):
        bag_stat = cPickle.load(open('../data/bags_ctr.pkl', 'rb'))
    else:
        bag_stat = {}
    # order format:adid,mid,ader,ad_industry_id,interact,pv
    with open(fpath, 'r') as fr:
        for line in fr:
            adid, mid, ader, ad_industry_id, interact, pv = line.strip().split()
            if int(pv) < 300:
                continue
            level = Bag_level(interact, pv)
            if ad_industry_id in bag_stat.keys():
                if level in bag_stat[ad_industry_id].keys():
                    bag_stat[ad_industry_id][level] += 1
                else:
                    bag_stat[ad_industry_id][level] = 1
            else:
                bag_stat[ad_industry_id] = {level: 1}
    cPickle.dump(bag_stat, open('../data/bags_ctr.pkl', 'wb'))
    print "finish BagProcess"


def main(words_path, order_path):
    WordsProcess(words_path)

# BagProcess(order_path)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "parameters erro:<words path><order path>"
    main(sys.argv[1], sys.argv[2])
