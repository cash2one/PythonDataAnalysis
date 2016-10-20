#coding=utf-8
import os
import cPickle
import commands
import MySQLdb
import datetime

class Upfans_Suggestion(object):
	"""docstring for upfans_suggestion"""
	def __init__(self,dir_path,order_data):
		super(Upfans_Suggestion, self).__init__()
		self.dir_path = dir_path
		self.order_data = order_data
		self.upfans_history_custom_record = set()
		self.upfans_custom_rpm_dic = {}
		self.mid_rpm = float(order_data['mid_rpm_week'])
		self.upfans_result = {}
		self.upfans_recmd_record = {}

	#check account headline: buy condition| return whether can buy
	def check_upfans_lushan(self,uid):
		servers=[['172.16.235.148','172.16.105.66'],
				['10.75.29.84','10.13.2.125'],
				['172.16.235.138','172.16.105.53'],
				['172.16.235.137','172.16.105.54'],
				['172.16.235.136','172.16.105.52'],
				['172.16.105.51','10.75.29.25']]
		#print int(uid)%6
	        servers_ip = servers[int(uid)%6]
	        record_flag = 0;
		#print int(uid)%6
		for ip in servers_ip:
			#print ip,uid
			strcmd = '''echo -n -e "get 1-'''+uid+'''\r\n" | nc '''+ip+" 9764"
			(status, output) = commands.getstatusoutput(strcmd)
			#type(status) int type(output) str /noresult: END---len(output):4
	                if status == 0 and len(output)>4:
	                        record_flag = 1
	                        break
	        return record_flag

	def upfans_sql(self,sql):
		conn= MySQLdb.connect(
	        	host='s4339i.hebe.grid.sina.com.cn',
		        port = 4339,
		        user='fansmore_r',
		        passwd='d958de40fd5dfe9',
		        db ='fansmore',
		        )
		cur = conn.cursor()
		cur.execute(sql)
		value = cur.fetchall()
		cur.close()
		conn.commit()
		conn.close()
		return value

	def upfans_history_custom_add(self):
		#table name 
	        now = datetime.datetime.now()
	        table_name = "fansmore_statistic_" + now.strftime("%y%m")
		#date working
	        date_working = datetime.date.today().strftime("\'%Y-%m-%d") + " 0:0:0\'"

	        sql="select uid from " + table_name + " where action_time >"+date_working +" limit 10 ;"
	        #print sql
		value = self.upfans_sql(sql)
		return [str(line[0]) for line in value]

	def upfans_history_custom(self):
		with open(self.dir_path+'/data/cust_uid.txt','r') as fr:
			for line in fr:
				self.upfans_history_custom_record.add(line.strip())
		new_custom_list = self.upfans_history_custom_add()
		for line in new_custom_list:
			if line not in self.upfans_history_custom_record:
				self.upfans_history_custom_record.add(line)
		return self.upfans_history_custom_record

	def upfan_recent_recmd(self):
		pass


	def upfans_history_rpm(self):
		with open(self.dir_path+"/data/custom_rpm.txt",'r') as fr:
			for line in fr:
				take = line.strip().split()
				if 'nan' == take[1]:
					continue
				self.upfans_custom_rpm_dic[take[0]] = float(take[1])

	#only used by emergency restore
	def upfans_recmd_record(self):
		#table begin 1504
		#with open(self.dir_path+"/data/upfans_recmd_record.txt")
		pass

	def data_store(self):
		cPickle.dump(self.upfans_history_custom_record,open(self.dir_path+'/data/upfans_history_custom_record.pkl','wb'))
		cPickle.dump(self.upfans_custom_rpm_dic,open(self.dir_path+'/data/upfans_custom_rpm_dic.pkl','wb'))
		cPickle.dump(self.upfans_recmd_record,open(self.dir_path+'/data/upfans_recmd_record.pkl','wb'))
		cPickle.dump(self.upfans_result,open(self.dir_path+'/data/upfans_result.pkl','wb'))


	def suggestion_result(self):
		#appearence location 
		self.upfans_history_rpm()
		self.upfans_history_custom()
		upfans_mod = 0
		upfans_mod_num = 1000
		mod_num = 100
		adid_mod = 0
		if os.path.isfile(self.dir_path+"/data/upfans_recmd_record.pkl"):
			self.upfans_recmd_record = cPickle.load(open(self.dir_path+"/data/upfans_recmd_record.pkl",'rb'))
		else:
			for i in range(upfans_mod_num):
				self.upfans_recmd_record[i] = {}
			if os.path.isfile(self.dir_path+"/data/upfans_recmd_record.txt"):
				with open(self.dir_path+"/data/upfans_recmd_record.txt",'r') as fr:
					for line in fr:
						take = line.strip().split('\t')
						upfans_mod = int(take[0])%upfans_mod_num
						self.upfans_recmd_record[upfans_mod][take[0]] = take[1]
		date_7 = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

		if os.path.exists(self.dir_path+'/data/upfans_result.pkl'):
			self.upfans_result = cPickle.load(open(self.dir_path+'/data/upfans_result.pkl','rb'))
		else:
			self.upfans_result ={}
			for i in range(mod_num):
				self.upfans_result[i] = {}
		#remove old
		order_set = set(self.order_data.keys())
		for k in self.upfans_result.keys():
			for adid in self.upfans_result[k].keys():
				if adid not in order_set:
					del self.upfans_result[k][adid]
		print "loop begin"
		i= 0
		upfans_custom_rpm_dic_set = set(self.upfans_custom_rpm_dic.keys())
		for (adid,values) in self.order_data.items():
			i +=1
			if adid.endswith('week'):
				continue
			adid_mod = int(adid)%mod_num
			if adid in self.upfans_result[adid_mod].keys():
				continue
			uid = values['ad_uid']
			buy_flag = self.check_upfans_lushan(uid)
			self.upfans_result[adid_mod][adid] = '0'
			#print "buy_flag:",adid,buy_flag
			if ( 1 == buy_flag):
				if uid in self.upfans_history_custom_record:
					if uid in upfans_custom_rpm_dic_set:
						if self.upfans_custom_rpm_dic[uid]>self.mid_rpm:
							self.upfans_result[adid_mod][adid] = '1'
				else:
					#print adid,self.upfans_recmd_record[uid],date_7,self.upfans_recmd_record[uid] < date_7
					upfans_mod = int(uid)%upfans_mod_num
					if uid not in self.upfans_recmd_record[upfans_mod].keys() or self.upfans_recmd_record[upfans_mod][uid] < date_7:
						#print adid,self.upfans_recmd_record[uid],date_7
						self.upfans_result[adid_mod][adid] = '2'
						self.upfans_recmd_record[upfans_mod][uid] = str(datetime.date.today())
		self.data_store()
		#print self.upfans_result
		return self.upfans_result

if __name__ == '__main__':
	order_data = cPickle.load(open('../data/order_data.pkl','rb'))
	myUpfansSuggestion = Upfans_Suggestion('../',order_data)
	myUpfansSuggestion.suggestion_result()
