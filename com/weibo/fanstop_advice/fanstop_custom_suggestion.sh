#!/bin/bash
source /etc/bashrc
CMD_PATH=$(cd `dirname $0`; pwd)
echo "current cmd path:$CMD_PATH"
cd ..
MAIN_PATH=`pwd`
echo $MAIN_PATH


time_now=`date "+%G-%m-%d %H:%M:%S"`
echo "RUNNING START TIME: $time_now"

python   $MAIN_PATH/script/main.py $MAIN_PATH #/data0/fans_economy/headline/chenwei9/fanstop_advice/
if [ $? -ne 0 ];then
	echo "main erro "
	python   $MAIN_PATH/script/main.py $MAIN_PATH
	if [ $? -ne 0 ];then
		exit 1
	fi
fi
echo "finish caculate"
mv $MAIN_PATH/data/out_data/update_data $MAIN_PATH/data/out_data/new_data
cat $MAIN_PATH/data/out_data/new_data $MAIN_PATH/data/out_data/no_update_data > $MAIN_PATH/data/out_data/candidate
python $MAIN_PATH/script/remove_repeat.py  #删除重复订单数据，当什么时候有重复订单?

#rsync $MAIN_PATH/data/out_data/candidate_data  /data0/fans_economy/headline/chenwei9 #在这个文件夹下，
rsync $MAIN_PATH/data/out_data/candidate_data_yizhou  /data0/fans_economy/headline/chenwei9 #在这个文件夹下，

time_now=`date "+%G-%m-%d %H:%M:%S"`
echo "RUNNING END TIME: $time_now"

#save order.txt
python $MAIN_PATH/script/order_data_out.py $MAIN_PATH

minus=`date +"%M"`
hour=`date +"%H"`
week=`date +%w`
if [[ "$hour" == "00" ]];then
	if [[ $minus > 30 ]];then
		rm -f $MAIN_PATH/script/fanstop_custom_suggestion_log.txt
		exit 0
	fi
    rsync -av /data0/fans_economy/follow_ratio/follow_ratio_30.txt $MAIN_PATH/data/custom_rpm.txt
    if [[ "$week" == "6" ]];then
        echo "week:${week}"
        f_path="/data0/fans_economy/headline/chenwei9/bowen_new_week.txt"
        if [ -f $f_path ];then
            echo "$f_path seg_words"
            mv $f_path $MAIN_PATH/data/bowen_new_week.txt
            seg_program="/data0/chenwei9/fanstop_data_suggestion/weiboseg/WeiboSegmentor-v2.3.4-el5.4-64bit-lib-20130304"
            ${seg_program}/example/TokenizerExampleCpp ${seg_program}/conf/tokenizer.conf -e utf-8 -g both -w -f  $MAIN_PATH/data/mid_content.txt  > $MAIN_PATH/data/online_words_weeks.txt
            python words_bags.py $MAIN_PATH/data/online_words_weeks.txt $MAIN_PATH/data/bags_weeks.txt
        fi
		rm -f $MAIN_PATH/script/fanstop_custom_suggestion_log.txt $MAIN_PATH/script/rsync_data_log.txt
		python $MAIN_PATH/script/ctr_week_avg.py $MAIN_PATH
		if [ -f "$MAIN_PATH/data/ctr_week_avg_update.txt" ];then
			echo "update ctr_avg_week $time_now"
			mv $MAIN_PATH/data/ctr_week_avg_update.txt $MAIN_PATH/data/ctr_week_avg.txt
		fi
    fi
	sql="select cat,count(1) from mds_ad_algo_fans_cat_target where dt='working' group by cat;"
	hive -e"$sql">$MAIN_PATH/data/bag_volume.txt
	tar -zcvf $MAIN_PATH/fanstop_advice_data_back.tar.gz $MAIN_PATH/data
	hadoop_back="/dw_ext/recmd/chenwei9/fanstop_advice_back"
	#备份数据到hdfs
	hadoop fs -rm -f $hadoop_back/fanstop_advice_data_back.tar.gz
	hadoop fs -put $MAIN_PATH/fanstop_advice_back.tar.gz $hadoop_back
fi
exit 0