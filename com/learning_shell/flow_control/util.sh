#!/usr/bin/env bash

#until循环执行一系列命令直至条件为真时停止。
#until循环与while循环在处理方式上刚好相反。
#一般while循环优于until循环，但在某些时候—也只是极少数情况下，until循环更加有用。

until condition
do
    command
done