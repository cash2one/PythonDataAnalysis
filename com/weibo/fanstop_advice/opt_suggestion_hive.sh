#!/bin/bash
source /etc/bashrc

date_end=`date -d"2 day ago" +"%Y%m%d"`
date_start=`date -d"9 day ago" +"%Y%m%d"`
echo $date_2

sql_drop="drop table if exists mds_ad_algo_fanstop_orientation_bowen_info;"

sql_create="create table if not exists mds_ad_algo_fanstop_orientation_bowen_info(
uid string comment 'customer uid',
mid string comment 'advertise mid',
industry_id string comment 'advertise buy orientation bags',
vtype  string comment 'ader vtype',
fans_num string comment 'ader fans number',
act_fans_num string comment 'ader fans number',
buy_count string comment 'buy expo  amount',
order_from string comment 'the order type',
huati_tag string,
content string,
url string,
image string,
video string,
music string)
partitioned by  (dt string)
row format  delimited fields terminated by '\t'
collection items terminated by ','
lines terminated by '\n'
stored as rcfile
location '/dw_ext/ad/person/chenwei9/working/mds_ad_algo_fanstop_orientation_bowen_info';"

date_working='test'
sql_data="insert overwrite table mds_ad_algo_fanstop_orientation_bowen_info partition (dt='${date_working}')
select cust_uid uid,mid,industry_id ,id_penfactor_type vtype ,fans_num,act_fans_num,count,order_from,huati_tag,content,if(find_filter(filter) like '%url%', 1,0),if(find_filter(filter) like '%image%', 1,0),if(find_filter(filter) like '%video%', 1,0),if(find_filter(filter) like '%music%', 1,0) from sds_ad_headline_report_order_industry_day a join ods_tblog_content b on a.feed_id = b.mid where count>=300 and b.dt>=${date_start} and b.dt<${date_end}';"

#sql_data="create table mds_ad_algo_fanstop_orientation_bowen_info as select cust_uid uid,mid,industry_id,id_penfactor_type vtype,fans_num,act_fans_num,count,order_from,huati_tag,content from sds_ad_headline_report_order_industry_day a join ods_tblog_content b on a.feed_id = b.mid where b.dt='20160701';"

sql_test="select order_id,cust_uid uid,industry_id,id_penfactor_type vtype ,fans_num,act_fans_num,count,order_from,feed_id from sds_ad_headline_report_order_industry_day where count>=300 and dt>='20160401'  and dt<'20160501';"
echo $sql_data
hive -e"${sql_drop}"
hive -e"${sql_create}"
hive -e"${sql_data}"
#hive -e"${sql_test}">../data/bowen_05.txt

##get distinct uid from HDSF: first time : all
#sql_all="
#select distinct cust_uid from sds_ad_upfans_report_order_day;
#"
#sql_add="select cust_uid from sds_ad_headline_report_order_industry_day join "
#hive -e"$sql_all">cust_uid.txt
##get orientation bag container 
#sql="
#select cat,count(1) from mds_ad_algo_fans_cat_target where dt='working' group by cat;"
#hive -e"$sql">bag_volume.txt

sql_train="select mid,industry_id,huati_tag,content from mds_ad_algo_fanstop_orientation_bowen_info where dt='test';"
hive -e"${sql_train}">../data/bowen_new_weeks.txt

#sql_train="select order_id,cust_uid,mid,'1601',industry_id,count from ds_ad_headline_report_order_industry_day where dt>='20160601';"
#hive -e"${sql_train}">../data/order_test.txt
