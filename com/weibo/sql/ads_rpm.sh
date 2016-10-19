#!/bin/bash
source /etc/bashrc


today=`date --date="$date 0 day ago" +%Y%m%d`
start_date='20160404'
folder_path='/data0/ads/yizhou/result/ads_rpm/'${today}
mkdir ${folder_path}
output_file_path=${folder_path}'/part-00000'
sql='SELECT 1, round(a.all_attend/a.all_pv,5) FROM (SELECT nvl(sum(CAST(pv AS float)),0) AS all_pv, nvl(sum(CAST(attend AS float)),0) AS all_attend FROM ads_algo_oid_uid_pv_attend_interaction WHERE cast(substring(dt,1,8) AS int) >=${start_date}) a UNION ALL SELECT a.uid, round(a.attend_float/a.pv_float,5) FROM (SELECT uid, nvl(sum(CAST(pv AS float)),0) AS pv_float, nvl(sum(CAST(attend AS float)),0) AS attend_float FROM ads_algo_oid_uid_pv_attend_interaction WHERE cast(substring(dt,1,8) AS int) >=${start_date} GROUP BY uid) a WHERE a.pv_float!=0'

hive -e "$sql" > ${output_file_path}

#check file size
size=ll ${output_file_path}|awk 'NR==1'|awk -F\  '{print $2}'
if [ ${size} -lt 700 ]
then
    echo "result  small than 700K, something error,exit...."
    echo "end...error..."${today}
    exit 1
fi
#rsync
rsync_path="10.39.1.50::headline_upload/account_ctr_predict/part-00000"
rsync -av --progress --port=9888 --bwlimit 20000 ${output_file_path} ${rsync_path}
if [ $? -eq 0 ];then
        echo "finish rsync train file"
        exit 0
fi
echo "rsync train file error"
exit 1