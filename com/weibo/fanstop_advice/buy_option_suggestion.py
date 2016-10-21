# -*- coding: utf-8 -*-
import cPickle as ce
import time
import datetime
import codecs
import sys
reload(sys) 
sys.setdefaultencoding('utf8')
class Buy_Option(object):
    """docstring for Buy_Option"""
    def __init__(self, dir_path,order_data,recmd_bags,bowen_result):
        super(Buy_Option, self).__init__()
        self.dir_path = dir_path
        self.order_data = order_data
        self.volume_dic = {}
        self.recmd_bags = recmd_bags
        self.bowen_result = bowen_result
        self.bag_name_dic = {}
        self.buy_result = {}

    #order data: order_id,uid,buy_code,each bag volume
    def buy_option(self,adid,adid_mod,values,nofans_volume,interest_bag,video_flag):
        #print values.keys()
        #print interest_bag
        #print values         
        flag = values['buy_type']
        if len(interest_bag)>0:
            tmpstr = self.bag_name_dic[interest_bag[0][0]]
        if 0 == flag:
            if values['fanstop_ctr'] > self.order_data[video_flag+'_fanstop_ctr_week']:
                if 0 == len(interest_bag):
                    self.buy_result[adid_mod][adid] = [1,u'推广效果很赞，试试投给潜在粉丝和兴趣用户，获取更多曝光和互动吧！']
                else:
                    self.buy_result[adid_mod][adid] = [1,u'推广效果很赞，试试投给潜在粉丝和对'+tmpstr+u'感兴趣的用户，获取更多曝光和互动吧！',interest_bag,0]
            else:
                if 0 == len(interest_bag):
                    self.buy_result[adid_mod][adid] = [0,u'本次推广还有不少优化空间，试试投给潜在粉丝和兴趣用户吧！']
                else:
                    self.buy_result[adid_mod][adid] = [0,u'本次推广还有不少优化空间，试试投给潜在粉丝和对'+tmpstr+u'感兴趣的用户吧！',interest_bag,0]
        elif 1 == flag:
            #print values.keys()
            if values['feifen_ctr'] > self.order_data[video_flag+'_feifen_ctr_week']:
                if values['feifen_maxnum'] != 0 and float(nofans_volume)/values['feifen_maxnum'] < 0.3:
                    if 0 == len(interest_bag):
                        self.buy_result[adid_mod][adid] = [1,u'推广效果很赞，试试投给兴趣用户和更多的潜在粉丝，获取更多曝光和互动吧！']
                    else:
                        self.buy_result[adid_mod][adid] = [1,u'推广效果很赞，试试投给潜在粉丝和对'+tmpstr+u'感兴趣的用户，获取更多曝光和互动吧！',interest_bag,0]
                else:
                    if 0 == len(interest_bag):
                        self.buy_result[adid_mod][adid] = [1,u'推广效果很赞，试试投给兴趣用户获取更多曝光和互动吧！']
                    else:
                        self.buy_result[adid_mod][adid] = [1,u'推广效果很赞，试试投给对'+tmpstr+u'感兴趣的用户获取更多曝光和互动吧！',interest_bag,1]

            else:
                if 0 == len(interest_bag):
                    self.buy_result[adid_mod][adid] = [0,u'本次推广还有不少优化空间，试试投给兴趣用户吧！']
                else:
                    self.buy_result[adid_mod][adid] = [0,u'本次推广还有不少优化空间，试试投给对'+tmpstr+u'感兴趣的用户吧！',interest_bag,1]
        elif 2 == flag:
            if values['orientation_ctr'] > self.order_data[video_flag+'_orientation_ctr_week']:
                if 0 == len(interest_bag):
                    self.buy_result[adid_mod][adid] = [1,u'推广效果很赞，试试投给潜在粉丝和更多的兴趣用户，获取更多曝光和互动吧！']
                else:
                    self.buy_result[adid_mod][adid] = [1,u'推广效果很赞，试试投给潜在粉丝和对'+tmpstr+u'感兴趣的用户，获取更多曝光和互动吧！',interest_bag,0]
            else:
                if 0 == len(interest_bag):
                    self.buy_result[adid_mod][adid] = [0,u'本次推广还有不少优化空间，试试投给潜在粉丝和其它兴趣用户吧！']
                else:
                    self.buy_result[adid_mod][adid] = [0,u'本次推广还有不少优化空间，试试投给潜在粉丝和对'+tmpstr+u'感兴趣的用户吧！',interest_bag,0]
        elif 3 == flag:
            if values['orientation_ctr'] > self.order_data[video_flag+'_orientation_ctr_week'] or values['feifen_ctr'] > self.order_data[video_flag+'_feifen_ctr_week']:
              #  print 'value:',values['orientation_ctr'],self.order_data[video_flag+'_orientation_ctr_week'],values['feifen_ctr'], self.order_data[video_flag+'_feifen_ctr_week']
                if values['feifen_maxnum'] != 0 and float(nofans_volume)/values['feifen_maxnum'] < 0.3:
                    if 0 == len(interest_bag):
                        self.buy_result[adid_mod][adid] = [1,u'推广效果很赞，试试投给更多的潜在粉丝和兴趣用户，获取更多曝光和互动吧！']
                    else:
                        self.buy_result[adid_mod][adid] = [1,u'推广效果很赞，试试投给更多的潜在粉丝和对'+tmpstr+u'感兴趣的用户，获取更多曝光和互动吧！',interest_bag,0]
                else:
                    if 0 == len(interest_bag):
                        self.buy_result[adid_mod][adid] = [1,u'推广效果很赞，再试试投给更多的兴趣用户，获取更多曝光和互动吧！']
                    else:
                        self.buy_result[adid_mod][adid] = [1,u'推广效果很赞，再试试投给对'+tmpstr+u'感兴趣的用户，获取更多曝光和互动吧！',interest_bag,1]
            else:
                if 0 == len(interest_bag):
                    self.buy_result[adid_mod][adid] = [0,u'本次推广还有不少优化空间，试试投给其它兴趣用户吧！']
                else:
                    self.buy_result[adid_mod][adid] = [0,u'本次推广还有不少优化空间，试试投给对'+tmpstr+u'感兴趣的用户吧！',interest_bag,1]

    def bag_volume(self):
        with open(self.dir_path+'/data/bag_volume.txt','r') as fr:
            for line in fr:
                take = line.strip().split()
                self.volume_dic[take[0]] = take[1]
    
    def bag_name(self):
        with open(self.dir_path+'/data/bag_name.txt','r') as fr:
            for line in fr:
                take = line.strip().split()
                self.bag_name_dic[take[0]] = take[1].decode('utf-8')

    def check_recmd_bags(self,adid):
        tmp =[]
        if adid in self.recmd_bags.keys():
            num_flag = 0
            for i in range(0,3):
                if len(self.recmd_bags[adid]['recmd_bags']) > 0:
                    #print self.recmd_bags[adid][bag_code]
                    if len(self.recmd_bags[adid]['recmd_bags']) < i+1:
                        break
                    try:
                        tmp.append([self.recmd_bags[adid]['recmd_bags'][i],self.recmd_bags[adid]['recmd_bags_v']])
                    except:
                        print self.recmd_bags[adid]
                        raise RuntimeError('check_recmd_bags error')
                    num_flag += 1
                    if 3 == num_flag:
                        break
        return tmp
    def buy_suggestion(self):
        print 'buy_suggestion begin: order num is ',len(self.order_data)
        self.bag_name()
        adid_mod_num = 100
        for (adid,values) in self.order_data.items():
            if adid.endswith('week'):
                continue
            #v -1: wheter video, -1:ctr,-3:feifen num,-4:buy_flag
            adid_mod = int(adid)%adid_mod_num
            ad_uid = values['ad_uid']
            interest_bag = self.check_recmd_bags(adid)
            nofans_volume = self.order_data[adid]['feifen_expo'] if 0 != self.order_data[adid]['feifen_expo'] else 0
            #print 'nofans_volume:',nofans_volume
            if adid_mod not in self.buy_result.keys():
                self.buy_result[adid_mod] = {}
            if adid_mod in self.bowen_result.keys() and adid in self.bowen_result[adid_mod].keys() and '1' == self.bowen_result[adid_mod][adid][1]:
                self.buy_option(adid,adid_mod,values,nofans_volume,interest_bag,'1')
            else:
                self.buy_option(adid,adid_mod,values,nofans_volume,interest_bag,'0')
        print 'buy_suggestion end: result num is ',len(self.buy_result)
        #ce.dump(self.buy_result,open('../data/buy_suggestion.pkl','wb'))
        print sum([len(i) for i in self.buy_result.values()])
        return self.buy_result

if __name__ == '__main__':
    order_data = ce.load(open('../data/order_data.pkl','rb'))
    bowen_result = ce.load(open('../data/bowen_advise.pkl','rb'))
    recmd_bags = ce.load(open('../data/recmd_bags.pkl','rb'))
    mybuy_suggestion = Buy_Option('../',order_data,recmd_bags,bowen_result)
    mybuy_suggestion.buy_suggestion()
