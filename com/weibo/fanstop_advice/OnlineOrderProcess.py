#encoding = utf-8
import os,sys,shutil
import datetime
import json
import re
import cPickle as ce
#############
#using for  check order up/down 
#

class OnlineOrderProcess(object):
	"""docstring for OnlineOrderPrecess"""
	def __init__(self, fpath_order,fpath_order_top,fpath_order_extend,fpath_out):
		super(OnlineOrderProcess, self).__init__()
		self.fpath_order = fpath_order
		self.fpath_order_top = fpath_order_top
		self.fpath_order_extend= fpath_order_extend
		self.fpath_out = fpath_out
		self.order = {}
		self.order_top = {}
		self.order_extend = {}
		self.order_record = {}
		self.history_order_record = {}
	def LoadOrderExtend(self):
		with open(self.fpath_order_extend,'r') as fr:
			for line in fr:
				adid,ad_uid,mid,time_f,bag_code,buy_num = line.strip().split()
				if adid in self.order_extend.keys():
					self.order_extend[adid]['bag_code'].append([bag_code,buy_num])
				else:
					self.order_extend[adid] = {'mid':mid}
					self.order_extend[adid]['bag_code'] = [[bag_code,buy_num]]
					self.order_extend[adid]['ad_uid'] = ad_uid

				if adid == '16081405019053000288':
					print 'order_extend:',self.order_extend['16081405019053000288']
	def LoadOrderTop(self):
		with open(self.fpath_order_top,'r') as fr:
			for line in fr:
				adid,ad_uid,mid,time_f = line.strip().split()
				if adid not in self.order.keys():
					self.order[adid] = {'mid':mid}
					self.order[adid]['buy_type'] = 0
					self.order[adid]['fanstop_num'] = 1  #mark buy fanstop
					self.order[adid]['feifen_num'] = 0
					self.order[adid]['orientation_num'] = 0
					self.order[adid]['feifen_maxnum'] = 0
					self.order[adid]['time_f'] = time_f
					self.order[adid]['o_flag'] = '0'
					self.order[adid]['ad_uid'] = ad_uid
					self.order[adid]['bag_code'] = []
					if adid == '16081405019053000288':
						print 'order top:',self.order['16081405019053000288']
	def LoadOrder(self):
		with open(self.fpath_order,'r') as fr:
			for line in fr:
				adid,ad_uid,mid,tmp_info = line.strip().split()
				time_f,o_flag,buy_num,buy_type = tmp_info.strip().split('|')
				if adid == '16081405019053000288':
					print line
				self.order[adid] = {'mid':mid}
				self.order[adid]['feifen_num'] = 0
				self.order[adid]['buy_type'] = 0
				self.order[adid]['orientation_num'] = 0
				self.order[adid]['fanstop_num'] = 0
				self.order[adid]['feifen_maxnum'] = 0
				self.order[adid]['time_f'] = time_f
				self.order[adid]['o_flag'] = o_flag
				self.order[adid]['ad_uid'] = ad_uid
				self.order[adid]['bag_code'] = []
				if 'f' == buy_type:
					self.order[adid]['fanstop_num'] = int(buy_num)
					self.order[adid]['buy_type'] = 0
				if 'o' == buy_type:
					buy_num,max_num = buy_num.split(',')
					self.order[adid]['feifen_maxnum'] = int(float(max_num))
					self.order[adid]['feifen_num'] = int(buy_num)
					self.order[adid]['buy_type'] = 1
				if 't' == buy_type:
					self.order[adid]['orientation_num'] = int(buy_num)
					self.order[adid]['bag_code'] = self.order_extend[adid]['bag_code']
					self.order[adid]['buy_type'] = 2
				if 'ot' == buy_type or 'to' == buy_type:
					buy_num,max_num = buy_num.split(',')
					self.order[adid]['bag_code'] = self.order_extend[adid]['bag_code']
					self.order[adid]['feifen_maxnum'] = int(float(max_num))
					self.order[adid]['orientation_num'] = sum([int(i[1]) for i in self.order_extend[adid]['bag_code']])
					self.order[adid]['feifen_num'] = int(buy_num) - self.order[adid]['orientation_num']
					self.order[adid]['buy_type'] = 3
				if adid == '16081405019053000288':
					 print 'order:',self.order['16081405019053000288']
	def OrderData(self):
		self.LoadOrderExtend()
		#need orientation bags info
		self.LoadOrder()
		#need feifen info
		self.LoadOrderTop()
		time_flag = str((datetime.datetime.now() + datetime.timedelta(hours=-20)))
		if os.path.exists('../data'):
			pass
		else:
			os.mkdir('../data')
		if os.path.exists('../data/order_record.pkl'):
			try:
				self.order_record = ce.load(open('../data/order_record.pkl','rb'))
				shutil.copyfile('../data/order_record.pkl','../data/order_record_back.pkl')
			except:
				self.order_record = ce.load(open('../data/order_record_back.pkl','rb'))
		else:
			self.order_record = {}
		for adid in self.order.keys():
			if adid not in self.order_record.keys() and isinstance(adid,basestring):
				self.order_record[adid] = self.order[adid]
				self.order_record[adid]['time'] = str(datetime.datetime.now())
			elif len(self.order_record[adid]['bag_code']) < len(self.order[adid]['bag_code']) or self.order[adid]['feifen_num']>self.order_record[adid]['feifen_num']: 
				if adid == '16081405019053000288':
					print "YES modify"
				self.order_record[adid] = self.order[adid]
				self.order_record[adid]['time'] = str(datetime.datetime.now())
		for adid in self.order_record.keys():
			if self.order_record[adid]['time'] < time_flag:
				del self.order_record[adid]
		with open(self.fpath_out,'w') as fw:
			for (adid,v) in self.order_record.items():
				if adid == '16081405019053000288':
					print "self.order_record:", self.order_record['16081405019053000288']
				if 0 == v['buy_type']:
					fw.write(adid+'\t'+v['ad_uid']+'\t'+v['mid']+'\t'+v['time_f']+'|'+v['o_flag']+'|'+str(v['fanstop_num'])+','+str(v['feifen_num'])+','+str(v['feifen_maxnum'])+'|f'+'\t'+'NULL'+'\n')
				elif 1 == v['buy_type']:
					fw.write(adid+'\t'+v['ad_uid']+'\t'+v['mid']+'\t'+v['time_f']+'|'+v['o_flag']+'|'+str(v['fanstop_num'])+','+str(v['feifen_num'])+','+str(v['feifen_maxnum'])+'|o'+'\t'+'NULL'+'\n')
				elif 2 == v['buy_type']:
					tb = []
					for ib in v['bag_code']:
						tb.append('-'.join(ib))
					fw.write(adid+'\t'+v['ad_uid']+'\t'+v['mid']+'\t'+v['time_f']+'|'+v['o_flag']+'|'+str(v['fanstop_num'])+','+str(v['feifen_num'])+','+str(v['feifen_maxnum'])+'|t'+'\t'+'|'.join(tb)+'\n')
				elif 3 == v['buy_type']:
					tb = []
					for ib in v['bag_code']:
						tb.append('-'.join(ib))
					fw.write(adid+'\t'+v['ad_uid']+'\t'+v['mid']+'\t'+v['time_f']+'|'+v['o_flag']+'|'+str(v['fanstop_num'])+','+str(v['feifen_num'])+','+str(v['feifen_maxnum'])+'|ot'+'\t'+'|'.join(tb)+'\n')
		ce.dump(self.order_record,open('../data/order_record.pkl','wb'))
		return self.order_record

	def LoadData(self):
		order_data = ce.load(open('../data/order_record.pkl','rb'))
		time_flag = str(datetime.datetime.now())
		with open('../data/order_data_check.txt','r') as fr:
			for line in fr:
				adid,ad_uid,mid,tmp_info,bag_info = line.strip().split('\t')
				time_f,o_flag,buy_num_info,buy_type = tmp_info.split('|')
				fanstop_num,feifen_num,feifen_maxnum = buy_num_info.split(',')
				if adid in order_data.keys():
					continue
				order_data[adid] = {}
				order_data[adid]['ad_uid'] = adid
				order_data[adid]['mid'] = mid
				order_data[adid]['fanstop_num'] = int(fanstop_num)
				order_data[adid]['feifen_num'] = int(feifen_num)
				order_data[adid]['feifen_maxnum'] = int(float(feifen_maxnum))
				order_data[adid]['orientation_num'] = 0
				order_data[adid]['bag_code'] = []
				order_data[adid]['time_f'] = time_flag
				if 't' not in buy_type:
					if 'o' in buy_type:
						order_data[adid]['buy_type'] = 1
					else:
						order_data[adid]['buy_type'] = 0
				else:
					if 'o' in buy_type:
						order_data[adid]['buy_type'] = 3
					else:
						order_data[adid]['buy_type'] = 2
				if 'NULL' != bag_info:
					for i in bag_info.split('|'):
						order_data[adid]['bag_code'].append(i.split('-')) 
					#print order_data[adid]['bag_code']
					for itm  in order_data[adid]['bag_code']:
						#print itm
						order_data[adid]['orientation_num'] = int(itm[1])+order_data[adid]['orientation_num']
		with open('../data/x','w') as fw:
			for (adid,values) in order_data.items():
				fw.write(adid+'\t'+json.dumps(values)+'\n')
		ce.dump(order_data,open('../data/order_record_check.pkl','wb'))
		print len(order_data)
		return order_data

if __name__ == '__main__':
	if len(sys.argv)<4:
		print "parameters ERRO: <adid_info.10><adid_top><fans_advance_extend><fpath_out>"
		sys.exit(1)
	myOnlineOrder = OnlineOrderProcess(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	order_data = myOnlineOrder.OrderData()
	print len(order_data)
	#myOnlineOrder.LoadData()
