#!/usr/bin/env bash

your_name="Zealot"
echo ${your_name}

for skill in Ada Coffe Action Java; do
    echo "I am good at ${skill}Script"
done

str="Hello, I know your are \"$your_name\"! \n"
str2='Hello, I know your are \"$your_name\"! \n' #强制原样输出

echo ${str}
echo ${str2}

greeting="hello, "${your_name}" !"
greeting_1="hello, ${your_name} !"
echo ${greeting} ${greeting_1}

#截取字符串
string="runoob is a great site"
echo ${string:1:4} # 输出 unoo


#查找字符 "i 或 s" 的位置：
string2="runoob is a great company"
echo `expr index "$string2" i`  # 输出 8

#数组
array_name=(value0 value1 value2 value3)
array_name=(
value0
value1
value2
value3
)
array_name[0]=value0
array_name[1]=value1
array_name[n]=valuen

echo ${array_name[*]} #输出整个数组
echo ${#array_name[@]} #输出数组长度

