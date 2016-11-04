#!/usr/bin/env bash

#-eq	等于则为真
#-ne	不等于则为真
#-gt	大于则为真
#-ge	大于等于则为真
#-lt	小于则为真
#-le	小于等于则为真

num1=100
num2=100
if test $[num1] -eq $[num2]
then
    echo '两个数相等！'
else
    echo '两个数不相等！'
fi