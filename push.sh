#!/bin/bash

if [ $# -lt 1 ];then
	echo "usage: push.sh file.sn"
	exit
fi
adb push $@ /tmp/
