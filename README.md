procScan.sh: 周期性地检测CPU使用情况和几个主要进程的内存使用情况，结果保存到/tmp/mem.txt文件；
topMem.py: 将mem.txt文件数据格式化，以点线图的方式画出表格；
结果获取(linux环境)：导出/tmp/mem.txt文件，与topMem.py放到同一目录下，运行topMem.py


执行：
./procScan.sh 数字 &
可以设置CPU检测和进程内存检测的时间周期，以秒为单位，例如：./procScan.sh 3，不带参数时默认时间周期为1秒

