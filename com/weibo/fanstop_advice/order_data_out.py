# -*- coding: utf-8 -*-

import cPickle as ce
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':

    dir_path = sys.argv[1]
    order_data = ce.load(open(dir_path + '/data/order_data.pkl', 'rb'))
    with open(dir_path + "/order_data_check.txt", 'w') as fw:
        for (adid, v) in order_data.items():
            if adid.endswith('week'):
                continue
            fw.write(adid + '\t' + json.dumps(v) + '\n')
