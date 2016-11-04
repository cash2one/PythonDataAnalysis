#!/usr/bin/env bash

echo "It is a test"
echo It is a test
echo "\"It is a test\""

#read 命令从标准输入中读取一行,并把输入行的每个字段的值指定给 shell 变量
#read name
#echo "$name It is a test"

echo -e "OK! \n" # -e 开启转义
echo "It it a test"

echo -e "OK! \c" # -e 开启转义 \c 不换行
echo "It is a test"


echo `date`