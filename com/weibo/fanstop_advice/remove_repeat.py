import os, sys
import json

# dir_path = "/data0/fans_economy/headline/chenwei9/fanstop_advice/data/out_data"
dir_path = "/data0/yizhou/cmd/opt_suggestion/fanstop_advice/data/out_data"
result_set = set()
result = {}
with open(dir_path + "/candidate", 'r') as fr:
    for line in fr:
        take = line.strip().split('\t')
        if len(take) < 2:
            print line
            continue
        if take[0] in result_set:
            continue
        else:
            result_set.add(take[0])
            try:
                result[take[0]] = take[1]
            except:
                continue
with open(dir_path + "/candidate_data_yizhou", 'w') as fw:
    for (k, v) in result.items():
        fw.write(k + '\t' + v + '\n')
