#!/usr/bin/env bash
# &&	逻辑的 AND	[[ $a -lt 100 && $b -gt 100 ]] 返回 false
# ||	逻辑的 OR	[[ $a -lt 100 || $b -gt 100 ]] 返回 true
a=10
b=20

if [[ $a -lt 100 && $b -gt 100 ]]
then
   echo "返回 true"
else
   echo "返回 false"
fi

if [[ $a -lt 100 || $b -gt 100 ]]
then
   echo "返回 true"
else
   echo "返回 false"
fi