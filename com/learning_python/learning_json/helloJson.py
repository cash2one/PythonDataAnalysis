__author__ = 'Zealot'

import json

obj = [[1,2,3],123,123.123,'abc',{'key1':(1,2,3),'key2':(4,5,6)}]
encodedjson = json.dumps(obj)
print repr(obj)
print encodedjson
a =  json.loads("{\"12\":12}")

s ='{\"12\":12, "name": 60}'
#s = '{"name": "ACME", "shares": 50, "price": 490.1}'
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

data = json.loads(s, object_hook=JSONObject)
print data.name

b={"6152772_原叶纯泡茶系列": ["1637070377_茉香绿茶", "1637070367_蜜香红茶", "1637075145_茉香绿茶", "1637075139_蜜香红茶"], "6152881_岩盐芝士系列": ["1637102039_岩盐芝士可可", "1637102029_岩盐芝士奶茶", "1637102009_岩盐芝士蜜香红茶", "1637102019_岩盐芝士绿茶", "1637104309_岩盐芝士可可", "1637104303_岩盐芝士奶茶", "1637104291_岩盐芝士蜜香红茶", "1637104297_岩盐芝士绿茶"], "6152689_雪乐冰系列": ["1637063210_红豆抹绿雪乐冰", "1637063200_柠檬优多雪乐冰", "1637063190_芒果优多雪乐冰"], "6152837_醇香心选系列": ["1637087045_蛋糕忌廉珍珠奶茶", "1637087021_OREO曲奇奶茶", "1637087039_红豆布丁烤奶茶", "1637087033_芋圆小丸子奶茶", "1637087015_大满贯布丁奶茶", "1637087003_原味奶茶", "1637087009_珍珠奶茶", "1637087027_烤珍珠奶茶", "1637132446_OREO曲奇奶茶", "1637132476_红豆布丁烤奶茶", "1637132466_芋圆小丸子奶茶", "1637132456_烤珍珠奶茶", "1637132486_蛋糕忌廉珍珠奶茶", "1637132426_珍珠奶茶", "1637132416_原味奶茶", "1637132436_大满贯布丁奶茶"], "6152645_养乐多系列": ["1637058560_养乐多绿茶", "1637058550_养乐多柠檬绿茶"], "6152606_额外附加品系列": ["1637056755_布丁", "1637056749_岩盐芝士", "1637056745_红豆", "1637056747_OREO", "1637056743_Q果", "1637056753_珍珠", "1637056751_小芋圆"], "6152739_茶拿铁系列": ["1637064454_珍珠茶拿铁", "1637064444_布丁茶拿铁", "1637064424_红豆茶拿铁", "1637064434_红茶拿铁", "1637068566_珍珠茶拿铁", "1637068548_红豆茶拿铁", "1637068560_布丁茶拿铁", "1637068554_红茶拿铁"], "6152924_清新柠檬系列": ["1637114797_金桔柠檬茶", "1637114779_手榨香柠蜜香红茶", "1637114791_柚恋柠檬茶", "1637114785_手榨香柠茉香绿茶", "1637132496_手榨香柠蜜香红茶", "1637132506_手榨香柠茉香绿茶", "1637132516_柠檬冰冻", "1637132526_柠檬Q果优多", "1637132536_柠檬菠萝冻", "1637132546_柚恋柠檬茶", "1637132556_金桔柠檬茶"], "6152801_多口感特调系列": ["1637076872_布丁可可", "1637076852_双柚Q果风味绿茶", "1637076832_芒橙Q果风味红茶", "1637076842_菠萝Q果风味红茶", "1637076862_芒橙Q果风味绿茶", "1637085978_布丁可可", "1637085960_菠萝Q果风味红茶", "1637085966_双柚Q果风味绿茶", "1637085954_芒橙Q果风味红茶", "1637085972_芒橙Q果风味绿茶"]}
bJson = json.loads(b, object_hook=JSONObject)
bJson



''''
商户转换成经营范围。一个商户会有多个标签，每个标签会对应一个权重。
1、通过商户id，找到商户名称，匹配到经营范围。
2、通过菜品名称，匹配到经营范围。
'''