__author__ = 'Zealot'
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
#contains 1.1
#beijing di qu
#add fu zhu ci biao
range_shop_map = {}
all_range = []
all_range_map = {}
with open("fu_zhu_ci_biao") as f:
    for line in f:
        fields = line.strip().split("\t")
        all_range.append(fields[0])
        range_name = fields[0]
        for index in fields[1:]:
            if index.strip() != "" and index != "\t":
                all_range_map[index] = range_name


for line in sys.stdin:
    fields = line.strip().split("\t")
    wid = fields[0]
    name = fields[1]

    res = [wid, name]
    # for key, value in range_shop_map.items():
    #     if name.find(key) != -1:
    #         res.extend(value)
    # if len(res) > 2:
    #     # pass
    #     print "\t".join(res)
    # else:
    flag = False
    for r_name in all_range_map.keys():
        if name.find(r_name) != -1:
            flag = True
            res.append(all_range_map[r_name])
    if flag:
        print "\t".join(res)

