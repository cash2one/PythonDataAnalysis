#!/bin/bash
source /etc/bashrc
hour=`date +"%H"`
week=`date +%w`
time_now=`date`
echo "RUNNING START TIME: $time_now"
#update data
python OnlineOrderProcess_v2.py /data0/fans_economy/headline/chenwei9/adid_dataprod ../data/order_data.txt
#python OnlineOrderProcess.py /data0/fans_economy/headline/chenwei9/adid_info.10 /data0/fans_economy/headline/chenwei9/adid_top /data0/fans_economy/headline/chenwei9/fans_advance_extend ../data/order_data.txt
#rsync -av /data0/fans_economy/headline/chenwei9/order_data.txt ../data/order_data.txt
echo "finish order combine"
time_now=`date`
echo "RUNNING END TIME: $time_now"
