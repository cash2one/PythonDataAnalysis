import cPickle as ce
import json

dir_path = "/data0/chenwei9/fanstop_data_suggestion"
dd = ce.load(open(dir_path + '/data/order_data.pkl', 'rb'))
with open(dir_path + "/order_data_check.txt", 'w') as fw:
    for (k, v) in dd.items():
        if k.endswith('week'):
            continue
        fw.write(k + '\t' + json.dumps(v) + '\n')
