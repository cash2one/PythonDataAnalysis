# coding=utf-8
import sys
import json
import os
import cPickle as ce
import threading
from weibo import *

reload(sys)

sys.setdefaultencoding('utf8')


class BowenSuggestion(object):
    """docstring for BowenSuggestion"""

    def __init__(self, dir_path, order_data):
        super(BowenSuggestion, self).__init__()
        self.dir_path = dir_path
        self.order_data = order_data
        self.bowen_result_all = []
        self.mid_record_dic_all = []

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
        #print 'video_flag',video_flag
        if pic_flag == 1:
            return 1, mid_content, video_flag
        else:
            return 0, mid_content, video_flag

    def short_url(self, mid_content):
        #print 'mid_content:',mid_content
        short_url = []
        if mid_content != '':
            flag_s = 0
            content = mid_content.split('\n')
            #print 'content:',content
            if len(content) > 1:
                mid_content = ' '.join(content)
            else:
                #print 'content[0]'
                mid_content = content[0]
            #print mid_content,'len mid_content:',len(mid_content)
            flag_e = len(mid_content)
            content = mid_content.split(' ')
            #print len(mid_content)
            for itm in content:
                mm = re.search('http://\w{1,}.*\w', itm)
                if mm != None:
                    test_url = mm.group()
                    #print 'http: YES',test_url
                    if len(test_url) > 20:
                        continue
                    tmp = 'url_short=' + test_url
                    #print tmp,len(tmp)
                    short_url.append(tmp)
        return short_url

    ##cycle check bowen | such as transmit include two parts
    def check_bowen_pic(self, line):
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

    def bowen_process(self, order_data_part, mid_record_dic, i):
        bowen_result = {}
        with open(self.dir_path + '/data/mid_content.txt' + str(i), 'w') as fw:
            for (k, v) in order_data_part.items():
                if k.endswith('week'):
                    continue
                mid = v['mid']
                if mid in mid_record_dic.keys():
                    bowen_result[k] = mid_record_dic[mid][0:2]
                    continue
                flag, mid_content, video_flag = self.get_bowen_info(int(mid))
                #if 0 != flag:
                dt_wk = str(datetime.date.today())
                bowen_result[k] = [flag, video_flag]
                #print 'bowen_result:',k,flag,video_flag
                fw.write(mid + '\t' + mid_content.replace("\n", " ") + '\n')
                #if 0 == flag:
                #	bowen_result[k] = [flag,video_flag]
                mid_record_dic[mid] = [flag, video_flag, dt_wk]
        self.bowen_result_all.append(bowen_result)
        self.mid_record_dic_all.append(mid_record_dic)

    def multi_task(self):
        #location_flag
        bowen_result = {}
        date_7 = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

        if os.path.exists(self.dir_path + "/data/mid_record_dic.pkl"):
            mid_record_dic = ce.load(open(self.dir_path + "/data/mid_record_dic.pkl", "rb"))
            for k in mid_record_dic.keys():
                if mid_record_dic[k][2] < date_7:
                    del mid_record_dic[k]
        else:
            mid_record_dic = {}
        #mid video card
        threads = []
        threads_iter = 0
        i = 0
        bath_num = len(self.order_data) / 5
        bath_dic = {}
        for (k, v) in self.order_data.items():
            if i % bath_num == 0 and i != 0:
                t = threading.Thread(target=self.bowen_process, args=(bath_dic, mid_record_dic, threads_iter))
                threads.append(t)
                t.start()
                bath_dic = {}
                threads_iter += 1
            i += 1
            bath_dic[k] = v
        if len(bath_dic) > 0:
            t = threading.Thread(target=self.bowen_process, args=(bath_dic, mid_record_dic, threads_iter))
            threads.append(t)
            t.start()
        for i in range(len(threads)):
            threads[i].join()

        for i in self.bowen_result_all:
            for (k, v) in self.bowen_result_all[i].items():
                if k not in bowen_result.keys():
                    bowen_result[k] = v
        for i in self.mid_record_dic_all:
            for (k, v) in self.mid_record_dic[i].items():
                if k not in mid_record_dic.keys():
                    mid_record_dic[k] = v
        print 'mid_record_dic num:', len(mid_record_dic)
        ce.dump(mid_record_dic, open(self.dir_path + "/data/mid_record_dic.pkl", 'wb'))
        return bowen_result

    def order_data_process(self):
        bowen_result = self.multi_task()
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
    myBoWen = BowenSuggestion("../", order_data)
    myBoWen.order_data_process()

