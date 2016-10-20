import cPickle as ce
import json
import sys, datetime

all_num = 0
recmd_num = 0
data = {}
with open(sys.argv[1], 'r') as fr:
    for line in fr:
        take = line.strip().split('\t');
        data[take[0]] = json.loads(take[1])

history_order = ce.load(open(sys.argv[2], 'rb'))

time_flag = str((datetime.datetime.now() + datetime.timedelta(hours=-96)))
print time_flag
history_set = set(history_order.keys())
for (k, v) in data.items():
    if k in history_set:
        if history_order[k]['time'] > time_flag:
            if len(v['orientationVol']) > 0:
                recmd_num += 1
            all_num += 1

print "recmd_num: ", recmd_num
print "all_num: ", all_num
