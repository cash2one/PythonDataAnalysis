#!/bin/bash
source /etc/bashrc
#每天创建新的文件夹
#执行hive脚本，到文件夹中，文件名为part-00000
#如果执行成功，则创建flag_done文件。在接下来的同步脚本中，来判断是否hive语句执行成功

today=`date +%Y-%m-%d`
start_date="20160404"
folder_path='/data0/ads/yizhou/result/ads_rpm/'${today}
mkdir ${folder_path}
output_file_path=${folder_path}"/part-00000"
sql="
set mapreduce.job.reduces=10;
SELECT 1 as aid,
       round(a.all_attend/a.all_pv,5) as rpm
FROM
  (SELECT nvl(sum(CAST(pv AS float)),0) AS all_pv,
          nvl(sum(CAST(attend AS float)),0) AS all_attend
   FROM ads_algo_oid_uid_pv_attend_interaction
   WHERE cast(substring(dt,1,8) AS int) >=${start_date}) a
UNION ALL
SELECT b.uid as aid,
       round(b.attend_float/b.pv_float,5) as rpm
FROM
  (SELECT uid,
          nvl(sum(CAST(pv AS float)),0) AS pv_float,
          nvl(sum(CAST(attend AS float)),0) AS attend_float
   FROM ads_algo_oid_uid_pv_attend_interaction
   WHERE cast(substring(dt,1,8) AS int) >=${start_date}
   GROUP BY uid) b
WHERE b.pv_float!=0"

hive -e "$sql" > ${output_file_path}

echo "out file:"${output_file_path}
echo "out sql:"${sql}

if [ $? -ne 0 ];then
 echo "hive sql erro : `date`"
 exit 255
fi
touch flag_done
