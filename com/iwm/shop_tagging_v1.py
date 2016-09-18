__author__ = 'Zealot'
import sys


reload(sys)
sys.setdefaultencoding("utf-8")

range_shop_map = {}
with open("shop_range_mapping") as f:
    for line in f:
        fields = line.strip().split("\t")
        range_shop_map.setdefault(fields[1], list())
        range_shop_map[fields[1]].append(fields[0])

for line in sys.stdin:
    fields = line.strip().split("\t")
    wid = fields[0]
    name = fields[1]

    res = [wid, name]
    for key, value in range_shop_map.items():
        if name.find(key) != -1:
            res.extend(value)
    if len(res) > 2:
        print "\t".join(res)

