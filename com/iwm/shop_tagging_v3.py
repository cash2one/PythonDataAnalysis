__author__ = 'Zealot'
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
#contains 1.1
#beijing di qu
#add fu zhu ci biao
#quchong
range_shop_map = {}
all_range = []
all_range_map = {}
with open("fu_zhu_ci_biao") as f:
    for line in f:
        fields = line.strip().split("\t")
        all_range.append(fields[0])
        range_name = fields[0]
        for index in fields[:]:
            if index.strip() != "" and index != "\t":
                all_range_map[index] = range_name


for line in sys.stdin:
    fields = line.strip().split("\t")
    wid = fields[0]
    name = fields[1]

    res = [wid, name]

    flag = False
    buf = []
    for r_name in all_range_map.keys():
        if name.find(r_name) != -1:
            flag = True
            buf.append(all_range_map[r_name])
    buf = set(buf)
    res.extend(buf)
    if flag:
        print "\t".join(res)

