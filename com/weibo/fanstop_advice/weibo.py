#!/usr/bin/python2.6
#coding=utf8

import socket
import base64
import urllib2
import json
#import memcache
import struct
import random
import copy
import time
import datetime
import re
#import redis

import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("/data0/fans_economy/headline/chenwei9/lib")

from call_openapi import get_open_api_data
weibo_api = "http://i2.api.weibo.com/2/statuses/show_batch.json?source=1780535200&ids="
weibo_api_url = "https://i2.api.weibo.com/2/short_url/expand.json?"
auth_user = "cuihua322@163.com"
auth_passwd = "1026322"

def request_api(api):
	try:
		socket.setdefaulttimeout(1.0)
		req = urllib2.Request(api)
		auth = base64.encodestring('%s:%s' % (auth_user, auth_passwd))[:-1]
		req.add_header("Authorization", "Basic %s"%auth)
		ret = urllib2.urlopen(req, timeout = 1.0).read()
		return ret
	except urllib2.URLError, e:
		return ''
	except urllib2.HTTPError, e:
		return ''
	except Exception, data:
		return ''

def request_weibo(mid):
	api = "%s%d"%(weibo_api, mid)

	ret = request_api(api)

	if ret == '':
		return None
	
	json_struct = json.loads(ret)
	return json_struct

def check_video(url):
	api = "%s%s"%(weibo_api_url,url)
	#print api
	try:
		ret = get_open_api_data(api, str(url))
	except:
		ret = ''
		print "api_connect erro"
	if ret == '':
		return 0
	#print ret
	video_list = ['video','youku.com','aqiyi.com','v.qq.com','tv.sohu.com','tudou.com','bilibili.com','pptv.com','letv.com','pps.tv','kankan.com','56.com']
	try:
		for itm in ret['urls']:
			for vf in video_list:
				if vf in  itm['url_long']:
					return 1
	except:
		print "check_video erro"
		return 0
	return 0

def check_pic_video(line):
	pic_flag = 0
	if "source" in line.keys():
		#print line['text']
		if "app" in line['source'].encode('utf-8'):
			pic_flag = 1
		if 'pic_ids' in line.keys() and len(line['pic_ids']) > 0:
			pic_flag = 1
		if "retweeted_status" in line.keys():
			pic_flag = check_pic_video(line["retweeted_status"])
	return pic_flag

if __name__ == '__main__':

	#json_struct = request_weibo(3995619703449270)
	check_video("url_short=http://t.cn/Rqa3knI&&url_short=http://t.cn/RtLlyQp&&url_short=http://t.cn/RtLi0kZ&&url_short=http://t.cn/Rty8I29")
	json_struct = request_weibo(3994910799620355)
	#print json_struct
	print check_pic_video(json_struct['statuses'][0])
	
