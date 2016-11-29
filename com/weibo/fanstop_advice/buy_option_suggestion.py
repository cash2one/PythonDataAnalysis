# -*- coding: utf-8 -*-
import cPickle as ce
import time
import datetime
import codecs
import sys_constant as sc
import sys
import utils as util
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

    def buy_option_v2(self, adid, adid_mod, values, nofans_volume, interest_bag, video_flag):
        buy_type = values['buy_type']
        interest_bag = ""
        interest_flag = 0
        if len(interest_bag) > 0:
            interest_bag = self.bag_name_dic[interest_bag[0][0]]
            interest_flag = 1

        fanstop_ctr = values['fanstop_ctr']
        feifen_ctr = values['feifen_ctr']
        orientation_ctr = values['orientation_ctr']
        sel_uid_ctr = values['sel_uid_ctr']
        fanstop_expo = values['fanstop_expo']
        feifen_expo = values['feifen_expo']
        orientation_expo = values['orientation_expo']
        sel_uid_expo = values['sel_uid_expo']

        fanstop_ctr_week = self.order_data[video_flag+'_fanstop_ctr_week']
        feifen_ctr_week = self.order_data[video_flag+'_feifen_ctr_week']
        orientation_ctr_week = self.order_data[video_flag+'_orientation_ctr_week']

        if video_flag+'_sel_uid_ctr_week' in self.order_data:
            sel_uid_ctr_week = self.order_data[video_flag+'_sel_uid_ctr_week']
        else:
            sel_uid_ctr_week = 0.01 if video_flag == 1 else 0.001
            # ini.logger.info("default param: " + str(sel_uid_ctr_week))


        # ini.logger.info("======start====================================================")
        is_high = self.is_high_interact_rating(fanstop_ctr, feifen_ctr, orientation_ctr, sel_uid_ctr, fanstop_expo,
                                               feifen_expo, orientation_expo, sel_uid_expo, fanstop_ctr_week,
                                               feifen_ctr_week, orientation_ctr_week, sel_uid_ctr_week)
        # ini.logger.info([fanstop_ctr, feifen_ctr, orientation_ctr, sel_uid_ctr, fanstop_expo,feifen_expo, orientation_expo, sel_uid_expo, fanstop_ctr_week,feifen_ctr_week, orientation_ctr_week, sel_uid_ctr_week])

        suggestion = self.get_suggestion_info_by_condition(buy_type, is_high, feifen_expo, nofans_volume, interest_bag)
        # ini.logger.info([adid, "buy_type: " + str(buy_type), " suggestion: " + suggestion])
        self.buy_result[adid_mod][adid] = [interest_flag, suggestion, interest_bag, 1 if sc.bowen_toutiao_sel_uid == buy_type else 0]
        # ini.logger.info("======end======================================================")


    def is_high_interact_rating(self, fanstop_ctr, feifen_ctr, orientation_ctr, sel_uid_ctr, fanstop_expo, feifen_expo, orientation_expo,
                          sel_uid_expo, fanstop_ctr_week, feifen_ctr_week, orientation_ctr_week, sel_uid_ctr_week):
        """
        计算当前广告的互动率是否高于平均的互动率：
                            (粉条ctr*粉条曝光占比*粉条7天平均ctr占比)
                            +(非粉ctr*非粉曝光占比*非粉7天平均ctr占比)
                            +(兴趣ctr*兴趣曝光占比*兴趣7天平均ctr占比)
                            +(指定账号ctr*指定账号曝光占比*指定账号7天平均ctr占比)

        :param fanstop_ctr:当天粉条ctr
        :param feifen_ctr:
        :param orientation_ctr:
        :param sel_uid_ctr:
        :param fanstop_expo: 粉条曝光
        :param feifen_expo:
        :param orientation_expo:
        :param sel_uid_expo:
        :param fanstop_ctr_week:粉条周平均ctr
        :param feifen_ctr_week:
        :param orientation_ctr_week:
        :param sel_uid_ctr_week:
        :return:
        """
        sum_ctr_week = fanstop_ctr_week + feifen_ctr_week + orientation_ctr_week + sel_uid_ctr_week
        sum_expo = fanstop_expo + feifen_expo + orientation_expo + sel_uid_expo #曝光总数
        w11, w12, w21, w22, w31, w32, w41, w42 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        if sum_expo and sum_ctr_week:
            w11 = float(fanstop_expo) / sum_expo
            w12 = float(fanstop_ctr_week) / sum_ctr_week
            w21 = float(feifen_expo) / sum_expo
            w22 = float(feifen_ctr_week) / sum_ctr_week
            w31 = float(orientation_expo) / sum_expo
            w32 = float(orientation_ctr_week) / sum_ctr_week
            w41 = float(sel_uid_expo) / sum_expo
            w42 = float(sel_uid_ctr_week) / sum_ctr_week

        a = fanstop_ctr * w11 * w12
        b = feifen_ctr * w21 * w22
        c = orientation_ctr * w31 * w32
        d = sel_uid_ctr * w41 * w42
        adid_rating = a + b + c + d
        #根据一周的ctr，与当前adid的系数，计算互动率
        sum_week_rating = fanstop_ctr_week * w11 * w12 + feifen_ctr_week * w21 * w22 + orientation_ctr_week * w31 * w32 + sel_uid_ctr_week * w41 * w42
        # print "buy_option_suggestion.py:159 ",w11, w12, w21, w22, w31, w32, w41, w42
        is_high = adid_rating > sum_week_rating
        # ini.logger.info([w11, w12, w21, w22, w31, w32, w41, w42, is_high])
        return adid_rating > sum_week_rating

    def get_suggestion_info_by_condition(self, buy_type, is_high, feifen_expo, feifen_maxnum, interest_bag):
        res = "本次推广还有不少优化空间，试试投给潜在粉丝、指定账号相似粉丝、兴趣用户和更多粉丝吧！"
        if not feifen_maxnum:
            return u''+res
        feifen_ratio = float(feifen_expo) / feifen_maxnum
        feifen_threshold = 0.3
        buy_type = int(buy_type)
        if buy_type == sc.bowen_toutiao_fanstop:
            res = "推广效果很赞，试试投给潜在粉丝、指定账号相似粉丝、兴趣用户和更多粉丝，获取更多曝光和互动吧！" if is_high else "本次推广还有不少优化空间，试试投给潜在粉丝、指定账号相似粉丝、兴趣用户和更多粉丝吧！"
        elif buy_type == sc.bowen_toutiao_feifen:
            if is_high and feifen_ratio < feifen_threshold:
                res = "推广效果很赞，试试投给粉丝、指定账号相似粉丝、兴趣用户和更多的潜在粉丝，获取更多曝光和互动吧！"
            elif is_high and feifen_ratio >= feifen_threshold:
                res = "推广效果很赞，试试投给粉丝、指定账号相似粉丝和兴趣用户获取更多曝光和互动吧！"
            else:
                res = "本次推广还有不少优化空间，试试投给粉丝、兴趣用户和指定账号相似粉丝吧！"
        elif buy_type == sc.bowen_toutiao_orientation:
            res = "推广效果很赞，试试投给粉丝、潜在粉丝、指定账号相似粉丝和更多兴趣用户，获取更多曝光和互动吧！" if is_high else "本次推广还有不少优化空间，试试投给粉丝、潜在粉丝、指定账号相似粉丝和其它兴趣用户吧！"
        elif buy_type == sc.bowen_toutiao_sel_uid:
            res = "推广效果很赞，试试投给粉丝、潜在粉丝、兴趣用户和更多指定账号相似粉丝，获取更多曝光和互动吧！" if is_high else "本次推广还有不少优化空间，试试投给粉丝、潜在粉丝、兴趣用户和其它指定账号相似粉丝吧！"
        elif buy_type == sc.bowen_toutiao_fanstop_feifen_orientation_sel_uid:
            if is_high and feifen_ratio < feifen_threshold:
                res = "推广效果很赞，试试投给更多粉丝、潜在粉丝、兴趣用户和指定账号相似粉丝，获取更多曝光和互动吧！"
            elif is_high and feifen_ratio >= feifen_threshold:
                res = "推广效果很赞，试试投给更多粉丝、兴趣用户和指定账号相似粉丝，获取更多曝光和互动吧！"
            else:
                res = "本次推广还有不少优化空间，试试投给其它兴趣用户、指定账号相似粉丝和更多粉丝吧！"
        elif buy_type == sc.bowen_toutiao_fanstop_feifen:
            if is_high and feifen_ratio < feifen_threshold:
                res = "推广效果很赞，试试投给兴趣用户、指定账号相似粉丝和更多粉丝、潜在粉丝，获取更多曝光和互动吧！"
            elif is_high and feifen_ratio >= feifen_threshold:
                res = "推广效果很赞，试试投给兴趣用户、指定账号相似粉丝和更多粉丝，获取更多曝光和互动吧！"
            else:
                res = "本次推广还有不少优化空间，试试投给更多粉丝、兴趣用户和指定账号相似粉丝吧！"
        elif buy_type == sc.bowen_toutiao_fanstop_orientation:
            res = "推广效果很赞，试试投给潜在粉丝、指定账号相似粉丝和更多粉丝、兴趣用户，获取更多曝光和互动吧！" if is_high else "本次推广还有不少优化空间，试试投给潜在粉丝、指定账号相似粉丝、更多粉丝和其它兴趣用户吧！"
        elif buy_type == sc.bowen_toutiao_fanstop_sel_uid:
            res = "推广效果很赞，试试投给潜在粉丝、兴趣用户和更多粉丝、指定账号相似粉丝，获取更多曝光和互动吧！" if is_high else "本次推广还有不少优化空间，试试投给潜在粉丝、兴趣用户、更多粉丝和其它指定账号相似粉丝吧！"
        elif buy_type == sc.bowen_toutiao_feifen_orientation:
            if is_high and feifen_ratio < feifen_threshold:
                res = "推广效果很赞，试试投给粉丝、指定账号相似粉丝和更多潜在粉丝、兴趣用户，获取更多曝光和互动吧！"
            elif is_high and feifen_ratio >= feifen_threshold:
                res = "推广效果很赞，试试投给粉丝、指定账号相似粉丝和其它兴趣用户，获取更多曝光和互动吧！"
            else:
                res = "本次推广还有不少优化空间，试试投给粉丝、指定账号相似粉丝和其它兴趣用户吧！"
        elif buy_type == sc.bowen_toutiao_feifen_sel_uid:
            if is_high and feifen_ratio < feifen_threshold:
                res = "推广效果很赞，试试投给粉丝、兴趣用户和更多潜在粉丝、指定账号相似粉丝，获取更多曝光和互动吧！"
            elif is_high and feifen_ratio >= feifen_threshold:
                res = "推广效果很赞，试试投给粉丝、兴趣用户和更多指定账号相似粉丝，获取更多曝光和互动吧！"
            else:
                res = "本次推广还有不少优化空间，试试投给粉丝、兴趣用户和其它指定账号相似粉丝吧！"
        elif buy_type == sc.bowen_toutiao_orientation_sel_uid:
            res = "推广效果很赞，试试投给粉丝、潜在粉丝和更多兴趣用户、指定账号相似粉丝，获取更多曝光和互动吧！" if is_high else "本次推广还有不少优化空间，试试投给粉丝、潜在粉丝和其它兴趣用户、指定账号相似粉丝吧！"
        elif buy_type == sc.bowen_toutiao_fanstop_feifen_orientation:
            if is_high and feifen_ratio < feifen_threshold:
                res = "推广效果很赞，试试投给指定账号相似粉丝和更多粉丝、潜在粉丝、兴趣用户，获取更多曝光和互动吧！"
            elif is_high and feifen_ratio >= feifen_threshold:
                res = "推广效果很赞，试试投给指定账号相似粉丝和更多粉丝、兴趣用户，获取更多曝光和互动吧！"
            else:
                res = "本次推广还有不少优化空间，试试投给指定账号相似粉丝和更多粉丝、其它兴趣用户吧！"
        elif buy_type == sc.bowen_toutiao_fanstop_feifen_sel_uid:
            if is_high and feifen_ratio < feifen_threshold:
                res = "推广效果很赞，试试投给兴趣用户和更多粉丝、潜在粉丝、指定账号相似粉丝，获取更多曝光和互动吧！"
            elif is_high and feifen_ratio >= feifen_threshold:
                res = "推广效果很赞，试试投给兴趣用户和更多粉丝、指定账号相似粉丝，获取更多曝光和互动吧！"
            else:
                res = "本次推广还有不少优化空间，试试投给兴趣用户、更多粉丝和其它指定账号相似粉丝吧！"
        elif buy_type == sc.bowen_toutiao_fanstop_orientation_sel_uid:
            res = "推广效果很赞，试试投给潜在粉丝和更多粉丝、兴趣用户、指定账号相似粉丝，获取更多曝光和互动吧！" if is_high else "本次推广还有不少优化空间，试试投给潜在粉丝、更多粉丝和其它兴趣用户、指定账号相似粉丝吧！"
        elif buy_type == sc.bowen_toutiao_feifen_orientation_sel_uid:
            if is_high and feifen_ratio < feifen_threshold:
                res = "推广效果很赞，试试投给粉丝和更多潜在粉丝、兴趣用户、指定账号相似粉丝，获取更多曝光和互动吧！"
            elif is_high and feifen_ratio >= feifen_threshold:
                res = "推广效果很赞，试试投给粉丝和更多兴趣用户、指定账号相似粉丝，获取更多曝光和互动吧！"
            else:
                res = "本次推广还有不少优化空间，试试投给粉丝和其它兴趣用户、指定账号相似粉丝吧！"
        else:
            res = "本次推广还有不少优化空间，试试投给潜在粉丝、指定账号相似粉丝、兴趣用户和更多粉丝吧！"

        #如果有兴趣包推荐，则添加兴趣包
        if len(interest_bag) > 0:
            interest_content = self.bag_name_dic[interest_bag[0][0]]
            res = res.replace("兴趣", "对" + interest_content + "感兴趣的")
        res = u''+res

        return res

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
                        tmp.append([self.recmd_bags[adid]['recmd_bags'][i], self.recmd_bags[adid]['recmd_bags_v']])
                    except:
                        print self.recmd_bags[adid]
                        raise RuntimeError('check_recmd_bags error')
                    num_flag += 1
                    # if 3 == num_flag:
                    #     break
        return tmp

    def buy_suggestion(self):
        util.logger.info(['buy_suggestion begin: order num is ', len(self.order_data)])
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
                self.buy_option_v2(adid,adid_mod,values,nofans_volume,interest_bag,'1')
            else:
                self.buy_option_v2(adid,adid_mod,values,nofans_volume,interest_bag,'0')
        util.logger.info(['buy_suggestion end: result num is ',len(self.buy_result)])
        # print sum([len(i) for i in self.buy_result.values()])
        util.logger.info([sum([len(i) for i in self.buy_result.values()])])
        return self.buy_result

if __name__ == '__main__':
    order_data = ce.load(open('../data/order_data.pkl', 'rb'))
    bowen_result = ce.load(open('../data/bowen_advise.pkl', 'rb'))
    recmd_bags = ce.load(open('../data/recmd_bags.pkl', 'rb'))
    mybuy_suggestion = Buy_Option('../', order_data, recmd_bags, bowen_result)
    mybuy_suggestion.buy_suggestion()
