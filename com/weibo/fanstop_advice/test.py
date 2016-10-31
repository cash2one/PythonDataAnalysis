__author__ = 'Zealot'
import __init__.logger as i
import cPickle as ce
i.info("123")
dir_path = "/data0/yizhou/cmd/opt_suggestion/fanstop_advice"
history_order_data = ce.load(open(dir_path + "/data/history_order_data.pkl", 'rb'))

map={}
map[0]=1
print map

for (adid, value) in history_order_data.items():
    if not adid.endswith('week'):
        buy_type = value["buy_type"]
        if buy_type in map.keys():
            map[buy_type] = map[buy_type] + 1
        else:
            map[buy_type]=1

print map
#
#
# i.info(map)