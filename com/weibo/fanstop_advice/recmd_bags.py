# encoding=utf-8
import os
import sys
import cPickle
import re
import codecs


class BagProb(object):
    """docstring for BagProb"""

    def __init__(self, dir_path, order_data):
        super(BagProb, self).__init__()
        self.dir_path = dir_path
        self.words_stat_path = dir_path + '/data/word_bags.pkl'
        self.bag_stat_path = dir_path + '/data/bags_ctr.pkl'
        self.words_bags_stat = {}
        self.bag_stat = {}
        self.order_data = order_data
        self.simi_data = {}
        self.midwords = {}
        self.bag_leve = {}
        self.special_bag = {'20003': '婚庆', '20007': '母婴', '20015': '养生', '20017': '减肥', '20019': '包包', '20020': '医疗',
                            '20021': '咖啡', '20022': '培训', '20024': '宠物', '20027': '戏剧', '20034': '文学', '20035': '文玩',
                            '20042': '烘焙', '20045': '童装', '20047': '红酒', '20048': '绘画', '20049': '美发', '20051': '育儿',
                            '20053': '茶', '20058': '鞋子', '20059': '音乐'}

    def LoadData(self):
        #check file exist
        if os.path.exists(self.words_stat_path) and os.path.exists(self.bag_stat_path):
            try:
                self.words_bags_stat = cPickle.load(open(self.words_stat_path, 'r'))
                self.bag_stat = cPickle.load(open(self.bag_stat_path, 'rb'))
            except Exception, e:
                raise RuntimeError("the runtime error: BagProb load data erro")
                sys.exit(1)
        else:
            raise RuntimeError("the runtime error: BagProb load data path erro")

    def ProbCaculate(self, words, bags, level):
        result = {}
        key_words = set(self.words_bags_stat.keys())
        #print words,type(key_words[0]), key_words[0:2],bags,level
        #print type(words)
        for bag in bags:
            p_w_b = 1.0
            word_num = 1
            for word in words:
                if word in key_words and bag in self.words_bags_stat[word].keys():
                    #print self.words_bags_stat[word]
                    p_w_b *= (1 + float(self.words_bags_stat[word][bag]) / sum(self.words_bags_stat[word].values()))
                    #print p_w_b,word_num
                    word_num += 1
            level_ratio = 1.35 if 2 == self.bag_leve[bag] else 1
            result[bag] = level_ratio * p_w_b * float(self.bag_stat[bag][str(level)]) / sum(self.bag_stat[bag].values())
        return result

    def Online_Words(self):
        with open(self.dir_path + '/data/online_words.txt', 'r') as fr:
            for line in fr:
                take = line.strip().split()
                mid = take[0].split(':')[0]
                for itm in take[2:]:
                    tk = itm.split(':')
                    if re.search('.*([0-9a-zA-Z]+).*', tk[0]) or int(tk[1]) < 10:
                        continue
                    if mid in self.midwords.keys():
                        self.midwords[mid].append(tk[0])
                    else:
                        self.midwords[mid] = [tk[0]]
                        #print tk[0]

    def Bag_Leve(self):
        with open(self.dir_path + '/data/ctr_classify.txt', 'r') as fr:
            for line in fr:
                take = line.strip().split()
                for itm in take[1:]:
                    self.bag_leve[itm] = int(take[0])

    def Bag_Recmd(self):
        bag_similar = {}
        bag_name = {}
        self.Bag_Leve()
        self.Online_Words()
        self.LoadData()
        with open(self.dir_path + '/data/bag_name.txt', 'r') as fr:
            for line in fr:
                take = line.strip().split()
                bag_name[take[0]] = take[1]
        with open(self.dir_path + '/data/bag_similar.txt', 'r') as fr:
            for line in fr:
                take = line.strip().split()
                bag_similar[take[0]] = take[1:]
        if os.path.exists(self.dir_path + '/data/recmd_bags.pkl'):
            result_dic = cPickle.load(open(self.dir_path + '/data/recmd_bags.pkl', 'rb'))
        else:
            result_dic = {}
        #remove old
        for k in result_dic.keys():
            if k not in self.order_data.keys():
                del result_dic[k]
        #fw2 = open(self.dir_path+'/data/cck.txt','w')
        for (adid, values) in self.order_data.items():
            if adid.endswith('week'):
                continue
            if 'bag_code' not in values.keys():
                print "not in bag_code dic"
                continue
            if adid in result_dic.keys():
                continue
            tmp_dic = {}
            mid = values['mid']
            #print values
            recmd_buy_num = 0
            midwords_set = set(self.midwords.keys())
            for itm in values['bag_code']:
                #print itm
                bag_code, buy_num = itm
                recmd_buy_num = int(buy_num) if int(buy_num) > recmd_buy_num else recmd_buy_num
                mid = values['mid']
                #fw2.write(adid+'\t'+bag_code+'\t'+buy_num+'\t'+bag_name[bag_code]+'\t')
                if int(buy_num) < 1 or mid not in midwords_set:
                    #fw2.write('\n')
                    #print "less than buy limits or online mid has\'t keywords"
                    continue
                if bag_code in bag_similar.keys():
                    bags_set = set(bag_similar[bag_code])
                for (k, v) in self.bag_leve.items():
                    if bag_code in self.bag_leve.keys() and v > self.bag_leve[bag_code]:
                        bags_set.add(k)
                candidate_bags = [i for i in bags_set]
                #print 'candidate_bags:',adid,candidate_bags
                tmp_result = self.ProbCaculate(self.midwords[mid], candidate_bags, self.bag_leve[bag_code])
                if len(tmp_result) == 0:
                    #fw2.write('\n')
                    continue
                #print tmp_result
                tmp_tuple = sorted(tmp_result.iteritems(), key=lambda d: d[1], reverse=True)
                #print tmp_tuple
                for i in tmp_tuple:
                    special_flag = 0
                    if '20003' == bag_code and '20008' == i[0]:
                        for ss_word in self.midwords[mid]:
                            if ss_word == '理财':
                                tmp_list.append(i[0])
                                special_flag = 1
                                break
                        if 0 == special_flag:
                            continue
                    if i[0] in self.special_bag.keys() and 0 == special_flag:
                        flag = 0
                        for ss_word in self.midwords[mid]:
                            if ss_word == self.special_bag[i[0]]:
                                flag = 1
                                break
                        if 0 == flag:
                            continue
                    tmp_dic[i[0]] = float(i[1])
                    if i[0] in bag_similar[bag_code]:
                        simi_flag = '1'
                    else:
                        simi_flag = '0'
                        #fw2.write(i[0]+':'+bag_name[i[0]]+' :value_'+str(i[1])+' :level_'+str(self.bag_leve[i[0]])+' :simi_'+simi_flag+'\t')
                        #fw2.write('\n')
            tmp = sorted(tmp_dic.iteritems(), key=lambda d: d[1], reverse=True)
            candi = []
            for i in range(0, len(tmp)):
                if i > 10:
                    break
                #print tmp[i][0]
                candi.append(tmp[i][0])
            #print 'candi:',candi
            result_dic[adid] = {'recmd_bags': candi, 'recmd_bags_v': recmd_buy_num}
            #remove repeat
            del_list = []
            result_dic_set = set(result_dic.keys())
            for itm in values['bag_code']:
                if adid in result_dic_set:
                    if 'recmd_bags' in result_dic[adid].keys():
                        for j in range(0, len(result_dic[adid]['recmd_bags'])):
                            if result_dic[adid]['recmd_bags'][j] == itm[0]:
                                del_list.append(j)
            del_list.sort()
            del_list.reverse()
            for i in range(0, len(del_list)):
                if i + 1 < len(del_list) and del_list[i] == del_list[i + 1]:
                    continue
                dl = del_list[i]
                try:
                    del result_dic[adid]['recmd_bags'][dl]
                except:
                    print "del_list:", del_list, 'recmd_bags:', result_dic[adid]['recmd_bags'], 'bag_code:', values[
                        'bag_code']
        #print "result_dic:",result_dic
        #fw2.close()
        cPickle.dump(result_dic, open(self.dir_path + '/data/recmd_bags.pkl', 'wb'))
        return result_dic


if __name__ == '__main__':
    if os.path.exists('../data/order_record.pkl'):
        order_data = cPickle.load(open('../data/order_record.pkl', 'rb'))
    else:
        raise RuntimeError('file erro: could not find order_record.pkl')
        sys.exit(1)
    myBagProb = BagProb('../', order_data)
    myBagProb.Bag_Recmd()






