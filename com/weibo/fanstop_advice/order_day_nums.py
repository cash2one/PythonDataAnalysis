import time
import datetime
import os
import sys
import cPickle as ce

def stat_day_nums(dir_path):
	order_path = dir_path+"/data/order_data.pkl"
	history_path = dir_path+"/data/history_order_data.pkl"
	if os.path.exists(order_path):
		order_data = ce.load(open(order_path,'rb'))
	else:
		order_data = {}
	if os.path.exists(history_path):
		history_data = ce.load(open(history_path,'rb'))
	else:
		history_data = {}
	day_f = str(datetime.date.today() + datetime.timedelta(days=-1))
	time_begin = str(datetime.date.today() + datetime.timedelta(days=-1)) + ' 00:00:0'
	time_end = str(datetime.date.today()) + ' 00:00:0' 
	order_num = 0
	for adid in order_data.keys():
		if adid.endswith('week'):
			continue
		if order_data[adid]['time'] < time_end  and order_data[adid]['time'] > time_begin:
			order_num += 1
	for adid in history_data.keys():
		if adid.endswith('week'):
			continue
		if history_data[adid]['time'] < time_end  and history_data[adid]['time'] > time_begin:
			order_num += 1
	print order_num

if __name__ == "__main__":
	if len(sys.argv)<1:
		print "parameters erro: please input file director"
		sys.exit(1)
	stat_day_nums(sys.argv[1])
