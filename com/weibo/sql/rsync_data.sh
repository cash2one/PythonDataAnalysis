#!/bin/bash

#判断是否hive脚本执行成功（通过flag_done文件）。
#检查执行结果大小是否正确。
#如果都成功，则发送数据。

today=`date +%Y-%m-%d`
folder_path='/data0/ads/yizhou/result/ads_rpm/'${today}
output_file_path=${folder_path}"/part-00000"


[ -f flag_done ] || { echo "erro: no new data:`date`"; exit 255; }
echo "rsync task begin:`date`"
rm -f flag_done
echo "check file size"

#check file size
size=`ll -h ${output_file_path}|awk 'NR==1'|awk -F\  '{print $5}'`
echo "out put file size: "${size}

if [ ${size} -lt 305980 ];then
    echo "result file size is too small, something error,exit...."
    echo "end...error..."${today}
    exit 1
fi
echo "check successfully..."
#rsync

rsync_path="10.39.1.50::headline_upload/account_ctr_predict/part-00000"
rsync -av --progress --port=9888 --bwlimit 20000 ${output_file_path} ${rsync_path}
if [ $? -eq 0 ];then
        echo "rsync ads rpm file successfully!"
        exit 0
fi
echo "rsync ads rpm error!"
exit 1

#/data0/ads/yizhou/cmd/ads_rpm.sh
#rsync_data.sh