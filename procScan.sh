#!/bin/sh

filePath="/tmp/mem.txt"

scanProcMemory(){
	for proc in "vispeech" "vifamily" "\/oem\/app\/flutter-gui\/gui_program\/mixpad_gui" "system_manager" "vicenter" "audio_manager" "guiservice" "mixpad_music" "\/oem\/ember-host\/bin\/ember-host" "dbus-daemon"
	do
		#ps:获取所有进程信息；grep:过滤掉影响下一条命令执行的内容；awk:提取目标数据
		pid=`ps -aux | grep -v "awk" | awk '/.*'$proc'.*/ {printf "%s ",$1}'`
		set -- $pid
		#there can be serval pids for a proc
		for item in $pid
		do
			mem=`cat /proc/$item/status | awk '{ if($1=="VmRSS:") printf "VmRSS=%s;",$2;else if($1=="VmData:") printf "VmData=%s",$2;}'`
			echo "$proc:$mem" >> $filePath
		done
		#cat /proc/$pid/status | awk '$1=="VmRSS:" {print "1:",$1,"2:",$2}'
	done
}

num=0
interval=1
if [ $# -ge 1 ];then
	interval=$1
fi
while :
do
	echo "$num times"
	let num++ 
	top -b -n 1 | awk '{ if($1=="Mem:") print $0;else if($1=="CPU:") print $0 }' >> $filePath
	scanProcMemory
	sleep $interval
done
