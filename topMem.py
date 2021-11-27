#!/usr/bin/python3
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
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


fp = open("./top.txt", "r", errors='ignore', encoding='utf-8')
line = fp.readline()
#data = set()
#data = list()
data = dict()
cpu_data = dict()

show_array = ['usr','sys','nic','idle','io','irq','sirq']
hide_array = ['nic','idle','irq','sirq','usr','sys']
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
            else:
                s += num
            if arr2[1] not in data:
                data[arr2[1]] = list()
            data[arr2[1]].append(num)
        total = free + used
        if 'sum' not in data:
            data['sum'] = list()
        data['sum'].append(s)
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
    line = fp.readline()
    if not line:
        print("not read content")
        break

fig = plt.figure()
a1 = fig.add_subplot(2,1,1)
a2 = fig.add_subplot(2,1,2)
for key in data:
    if key not in hide_array:
        a1.plot(data[key], label = key)
    """
    num = max(data[key])
    if(num<80000):
        print(key + ":", max(data[key]))
        a1.plot(data[key], label = key)
    else:
        print(key + ":", max(data[key]))
        a2.plot(data[key], label = key)
    """

for key in cpu_data:
    if key not in hide_array:
        a2.plot(cpu_data[key], label = key)

y_major_locator=MultipleLocator(5000)
a1.yaxis.set_major_locator(y_major_locator)
a1.legend()
a2.legend()
plt.show()
