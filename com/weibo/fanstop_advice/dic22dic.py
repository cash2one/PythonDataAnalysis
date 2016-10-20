import cPickle as ce

upfans_mod = 0
upfans_mod_num = 1000
dir_path = '../'
upfans_recmd_record = ce.load(open(dir_path + "/data/upfans_recmd_record.pkl", 'rb'))
upfans_recmd_record_new = {}
for i in range(upfans_mod_num):
    upfans_recmd_record_new[i] = {}
for (k, v) in upfans_recmd_record.items():
    upfans_mod = int(k) % upfans_mod_num
    upfans_recmd_record_new[upfans_mod][k] = v
upfans_recmd_record = upfans_recmd_record_new

ce.dump(upfans_recmd_record_new, open(dir_path + '/data/upfans_recmd_record.pkl', 'wb'))

upfans_result = ce.load(open(dir_path + '/data/upfans_result.pkl', 'rb'))
adid_mod_num = 100

upfans_result_new = {}
for i in range(adid_mod_num):
    upfans_result_new[i] = {}
for (k, v) in upfans_result.items():
    adid_mod = int(k) % adid_mod_num
    upfans_result_new[adid_mod][k] = v
ce.dump(upfans_result_new, open(dir_path + '/data/upfans_result.pkl', 'wb'))

mid_mod_num = 1000
mid_record_dic = ce.load(open(dir_path + "/data/mid_record_dic.pkl", "rb"))
mid_record_new = {}
for i in range(mid_mod_num):
    mid_record_new[i] = {}
for (k, v) in mid_record_dic.items():
    k_mod = int(k) % mid_mod_num
    mid_record_new[k_mod][k] = v
print len(mid_record_new[10].keys()), len(mid_record_new)
ce.dump(mid_record_new, open(dir_path + "/data/mid_record_dic.pkl", 'wb'))







