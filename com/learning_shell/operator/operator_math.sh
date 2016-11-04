#!/usr/bin/env bash


# +	加法	`expr $a + $b` 结果为 30。
# -	减法	`expr $a - $b` 结果为 -10。
# *	乘法	`expr $a \* $b` 结果为  200。
# /	除法	`expr $b / $a` 结果为 2。
# %	取余	`expr $b % $a` 结果为 0。
# =	赋值	a=$b 将把变量 b 的值赋给 a。
# ==	相等。用于比较两个数字，相同则返回 true。	[ $a == $b ] 返回 false。
# !=	不相等。用于比较两个数字，不相同则返回 true。	[ $a != $b ] 返回 true。

val=`expr 2 + 2`
echo "两数之和为 : $val"

a=10
b=20

val=`expr $a + $b`
echo "a + b : $val"

val=`expr $a - $b`
echo "a - b : $val"

val=`expr $a \* $b`
echo "a * b : $val"

val=`expr $b / $a`
echo "b / a : $val"

val=`expr $b % $a`
echo "b % a : $val"

if [ $a == $b ]
then
   echo "a 等于 b"
fi
if [ $a != $b ]
then
   echo "a 不等于 b"
fi



