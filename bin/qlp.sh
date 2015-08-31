#!/bin/bash

ps aux | grep -i qore-l - | cut -d' ' -f7 | xargs kill -9 
ps aux | grep -i qore-l - | cut -d' ' -f7 | xargs kill -9 
ps aux | grep -i qore-l - | cut -d' ' -f6 | xargs kill -9 
ps aux | grep -i qore-l - | cut -d' ' -f6 | xargs kill -9

addr=`ifconfig | grep -i inet - | grep -i addr - | grep -i Bcast - | cut -d' ' -f15 | cut -d':' -f2`
addr=`ifconfig | grep -i inet - | grep -i addr - | grep -i Bcast - `

echo $addr | cut -d' ' -f09 #| cut -d':' -f2
echo $addr | cut -d' ' -f10 #| cut -d':' -f2
echo $addr | cut -d' ' -f11 #| cut -d':' -f2
echo $addr | cut -d' ' -f12 #| cut -d':' -f2
echo $addr | cut -d' ' -f13 #| cut -d':' -f2
echo $addr | cut -d' ' -f14 #| cut -d':' -f2
echo $addr | cut -d' ' -f15 #| cut -d':' -f2
echo $addr | cut -d' ' -f16 #| cut -d':' -f2
echo $addr | cut -d' ' -f17 #| cut -d':' -f2
echo $addr | cut -d' ' -f18 #| cut -d':' -f2
echo $addr | cut -d' ' -f19 #| cut -d':' -f2
echo $addr | cut -d' ' -f20 #| cut -d':' -f2
echo $addr | cut -d' ' -f21 #| cut -d':' -f2
echo $addr | cut -d' ' -f22 #| cut -d':' -f2
echo 'addr'
echo $addr
ipython notebook --ip=$addr
