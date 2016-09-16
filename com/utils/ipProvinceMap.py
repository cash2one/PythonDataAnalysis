#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys
import cidrtire

reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    ipCityFile = 'isp_ip_yyt.csv'
    index = {}
    trie = cidrtire.CIDRtrie()
    with open(ipCityFile) as f:
        for line in f:
            tmpList = line.strip().split(',')
            ip = tmpList[0]
            index[ip] = tmpList[-1]
            overwrite = trie.add_cidr(ip)

    with open('2014_2015_2016_user.csv') as f:
        for line in f:
            tmpList = line.strip().split(',')
            ip = tmpList[6]

            try:
                cidr = trie.get_cidr(ip)
            except:
                continue
            if cidr:
                area = index[cidr]
                print ','.join([line,  area])
            else:
                print ','.join([line,  "其他"])
