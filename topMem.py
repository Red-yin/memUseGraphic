#!/usr/bin/python3
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib import dates

import os
import sys
import time

class DataFormat:
    def __init__():
        pass

class DataInput:
    def __init__():
        pass

class DataDraw:
    def __init__():
        pass

print(sys.argv)
file_path = "./mem.txt"
if len(sys.argv) > 1:
    file_path = sys.argv[1]

fp = open(file_path, "r", errors='ignore', encoding='utf-8')
line = fp.readline()
#data = set()
#data = list()
data = dict()
cpu_data = dict()
mem_data = dict()
time_data = dict()

show_array = ['usr','sys','nic','idle','io','irq','sirq']
hide_array = ['nic','idle','irq','sirq','usr','sys']
#proc_array = ["vispeech","/oem/app/flutter-gui/gui_program/mixpad_gui","vicenter","audio_manager"]
proc_array = ["vispeech","vifamily","mixpad_gui","system_manager","vicenter","audio_manager","guiservice","mixpad_music","ember-host","dbus-daemon"]
proc_mem_names = ["VmRSS", "VmData"]
#['usr','sys','nic','idle','io','irq','sirq']
#['used','free','shrd','buff','cached']

while line is not None:
    if line.find('Mem:') != -1:
        arr0 = line.split(':')
        arr1 = arr0[1].split(',')
        s = 0
        free = 0
        used = 0
        for item in arr1:
            arr2 = item.split(  )
            num = int(arr2[0].strip('K'))
            if(arr2[1] == 'used'):
                used = num
            elif(arr2[1] == 'free'):
                free = num
                continue
            if arr2[1] not in data:
                data[arr2[1]] = list()
            data[arr2[1]].append(num)
        total = free + used
        if 'total' not in data:
            data['total'] = list()
        data['total'].append(total)
    elif line.find('CPU:') != -1:
        arr0 = line.split(':')
        #for c in arr0[1]:
            #print(hex(ord(c)))
        arr1 = arr0[1].split('  ')
        for item in arr1:
            arr2 = item.split()
            if len(arr2) < 2:
                continue
            if arr2[1] not in cpu_data:
                cpu_data[arr2[1]] = list()
            num = int(arr2[0].strip('%'))
            cpu_data[arr2[1]].append(num)
    elif line.find('stamp') != -1:
        if line.startswith('datestamp'):
            #日期记录数据
            arr0 = line.split(': ')
            if len(arr0) < 2:
                continue
            arr1 = arr0[1].split()
            if len(arr1) < 4:
                continue
            if 'datestamp' not in time_data:
                time_data['datestamp'] = list()
            time_data['datestamp'].append(arr1[3])
        elif line.startswith('timestamp'):
            #时间戳记录数据
            arr0 = line.split(':')
            if len(arr0) < 2:
                continue
            if 'timestamp' not in time_data:
                time_data['timestamp'] = list()
            time_data['timestamp'].append(arr0[1])
    else:
        for name in proc_array:
            if line.find(name) != -1:
                if name not in mem_data:
                    mem_data[name] = dict()
                arr0 = line.split(':')
                arr1 = arr0[1].split(';')
                s = 0
                for m in arr1:
                    arr2 = m.split('=')
                    if len(arr2) < 2:
                        continue
                    if arr2[0] not in mem_data[name]:
                        mem_data[name][arr2[0]] = list()
                    num = int(arr2[1].strip('\n'))
                    mem_data[name][arr2[0]].append(num)



    line = fp.readline()
    if not line:
        print("not read content")
        break


#print("format data: ", mem_data)
fig = plt.figure()
#a1 = fig.add_subplot(3,1,1)
#a2 = fig.add_subplot(3,1,2)
a3 = fig.add_subplot(1,1,1)
for key in data:
    if key in hide_array:
        continue
    #a1.plot(data[key], label = key)
    """
    num = max(data[key])
    if(num<80000):
        print(key + ":", max(data[key]))
        a1.plot(data[key], label = key)
    else:
        print(key + ":", max(data[key]))
        a2.plot(data[key], label = key)
    """

    """
for key in cpu_data:
    if key not in hide_array:
        a2.plot(cpu_data[key], label = key)

    """
color_array = ["aliceblue", "black", "blue", "brown", "coral", "tomato", "pink", "yellow", "green", "red", "gray"]
i = 0
for key in mem_data:
    i = i+1
    vm = "VmRSS" 
    #vm = "VmData"
    l = len(mem_data[key][vm])
    t_len = len(time_data['datestamp'])
    while len(time_data['datestamp']) > l:
        time_data['datestamp'].pop()
    while len(mem_data[key][vm]) > t_len:
        mem_data[key][vm].pop()
    a3.plot(time_data['datestamp'], mem_data[key][vm], label = key+"." + vm, color = color_array[i])
    """
    for k in mem_data[key]:
        a3.plot(mem_data[key][k], label = key+"."+k, color = color_array[i])
    """

x_major_locator=MultipleLocator(180)
y_major_locator=MultipleLocator(1000)
#a1.yaxis.set_major_locator(y_major_locator)
#a1.legend()
#a2.legend()
a3.yaxis.set_major_locator(y_major_locator)
a3.xaxis.set_major_locator(x_major_locator)
a3.legend()
plt.ylim(100, 220000)
a3.grid()
plt.show()
