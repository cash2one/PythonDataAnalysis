#!/usr/bin/env bash

int=1
while(( $int<=5 ))
do
        echo $int
        let "int++"
done