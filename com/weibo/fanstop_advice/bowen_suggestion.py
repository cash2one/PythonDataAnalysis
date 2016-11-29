# coding=utf-8
import sys
import json
import os
import cPickle as ce
from weibo import *

reload(sys)

sys.setdefaultencoding('utf8')


class BowenSuggestion(object):
    """docstring for BowenSuggestion"""

    def __init__(self, dir_path, order_data):
        super(BowenSuggestion, self).__init__()
        self.dir_path = dir_path
        self.order_data = order_data

    #order_data bowen info and return whether have picture
    def get_bowen_info(self, mid):
        json_result = request_weibo(mid)
        if json_result is None or len(json_result) == 0 or len(json_result['statuses']) == 0:
            return -1, 'NULL', '1'
        pic_flag, mid_content, video_flag = self.check_bowen_pic(json_result['statuses'][0])
        url_list = self.short_url(mid_content)
        if len(url_list) > 0:
            url_test = '&&'.join(url_list)
            video_flag = check_video(url_test)
        else:
            video_flag = 0
        if pic_flag == 1:
            return 1, mid_content, video_flag
        else:
            return 0, mid_content, video_flag

    def short_url(self, mid_content):#博文当中是否包含短链接
        short_url = []
        if mid_content != '':
            flag_s = 0
            content = mid_content.split('\n')
            if len(content) > 1:
                mid_content = ' '.join(content)
            else:
                mid_content = content[0]
            flag_e = len(mid_content)
            content = mid_content.split(' ')
            for itm in content:
                mm = re.search('http://\w{1,}.*\w', itm)
                if mm != None:
                    test_url = mm.group()
                    if len(test_url) > 20:
                        continue
                    tmp = 'url_short=' + test_url
                    short_url.append(tmp)
        return short_url

    ##cycle check bowen | such as transmit include two parts
    def check_bowen_pic(self, line):#检查博文当中是否有图片、视频、内容
        pic_flag = 0
        mid_content = ''
        video_flag = '0'
        if "source" in line.keys():
            mid_content = mid_content + line['text']
            if "头条文章" in line['text'].encode('utf-8'):
                return 1, mid_content, '1'
            if 'pic_ids' in line.keys() and len(line['pic_ids']) > 0:
                return 1, mid_content, '1'
            if "retweeted_status" in line.keys():
                pic_flag, tmp_txt, video_flag = self.check_bowen_pic(line["retweeted_status"])
                mid_content = mid_content + tmp_txt
        return pic_flag, mid_content, video_flag

    def bowen_process(self):
        #location_flag
        bowen_result = {}
        mid_mod_num = 1000
        key_mod_num = 100
        date_7 = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        dt_wk = str(datetime.date.today())
        if os.path.exists(self.dir_path + "/data/mid_record_dic.pkl"):
            mid_record_dic = ce.load(open(self.dir_path + "/data/mid_record_dic.pkl", "rb"))
            for k in mid_record_dic.keys():
                if len(mid_record_dic[k].keys()) == 0:
                    continue
                for mid in mid_record_dic[k].keys():
                    if mid_record_dic[k][mid][2] < date_7:
                        del mid_record_dic[k][mid]
        else:
            mid_record_dic = {}
            for i in range(mid_mod_num):
                mid_record_dic[i] = {}
        #mid video card
        with open(self.dir_path + '/data/mid_content.txt', 'w') as fw:
            for (k, v) in self.order_data.items():
                if k.endswith('week'):
                    continue
                mid = v['mid']
                k_mod = int(k) % key_mod_num
                mid_mod = int(mid) % mid_mod_num
                if k_mod not in bowen_result.keys():
                    bowen_result[k_mod] = {}
                if mid_mod in mid_record_dic.keys() and mid in mid_record_dic[mid_mod].keys():
                    bowen_result[k_mod][k] = mid_record_dic[mid_mod][mid][0:2]
                    continue
                flag, mid_content, video_flag = self.get_bowen_info(int(mid))
                bowen_result[k_mod][k] = [flag, video_flag]
                fw.write(mid + '\t' + mid_content.replace("\n", " ") + '\n')
                mid_record_dic[mid_mod][mid] = [flag, video_flag, dt_wk]
        print 'mid_record_dic num:', len(mid_record_dic)
        ce.dump(mid_record_dic, open(self.dir_path + "/data/mid_record_dic.pkl", 'wb'))
        return bowen_result

    def order_data_process(self):
        bowen_result = self.bowen_process()
        ce.dump(bowen_result, open(self.dir_path + "/data/bowen_advise.pkl", 'wb'))
        #with open(self.dir_path+'/data/bowen_advise.txt','w') as fw:
        #	for (k,v) in bowen_result.items():
        #		fw.write(k+'\t'+','.join(v)+'\n')
        print "bowen order data num:", len(self.order_data)
        print "bowen result num:", len(bowen_result)
        return bowen_result


if __name__ == '__main__':
    # main(sys.argv[1])
    order_data = ce.load(open('../data/order_record.pkl', 'rb'))
    myBoWen = BowenSuggestion('../', order_data)
    myBoWen.order_data_process()

