#!/usr/bin/python3
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib.pyplot import LinearLocator
from matplotlib import dates

import os
import sys
import time
import re

def VmRSS_VmData_cbk(line):
    ret_d = dict()
    arr0 = line.split(':')
    if len(arr0) < 2:
        print(line)
        return ret_d
    name = arr0[0]
    ret_d[name] = dict()
    arr1 = arr0[1].split(';')
    s = 0
    for m in arr1:
        arr2 = m.split('=')
        if len(arr2) < 2:
            continue
        num = int(arr2[1].strip('\n'))
        ret_d[name][arr2[0]] = num

    return ret_d

def datestamp_cbk(line):
    ret_d = dict()
          #日期记录数据
    arr0 = line.split(': ')
    if len(arr0) < 2:
        print(line)
        return ret_d
    arr1 = arr0[1].split()
    if len(arr1) < 4:
        print(line)
        return ret_d
    ret_d['datestamp'] = arr1[3]
 
    return ret_d

def timestamp_cbk(line):
    ret_d = dict()
        #时间戳记录数据
    arr0 = line.split(':')
    if len(arr0) < 2:
        print(line)
        return ret_d
    ret_d['timestamp'] = arr0[1]
   
    return ret_d

def CPU_cbk(line):
    ret_d = dict()
    arr0 = line.split(':')
        #for c in arr0[1]:
            #print(hex(ord(c)))
    arr1 = arr0[1].split('  ')
    for item in arr1:
        arr2 = item.split()
        if len(arr2) < 2:
            #print(line)
            continue
        num = int(arr2[0].strip('%'))
        ret_d[arr2[1]] = num
 
    return ret_d

def Mem_cbk(line):
    ret_d = dict()
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
        ret_d[arr2[1]] = num
    total = free + used
    ret_d['total'] = total
    return ret_d

def orb_log_cbk(line):
    ret_d = dict()
    arr0 = line.split()
    if len(arr0) < 2:
        print(line)
        return ret_d
    cpu_array = arr0[4].split(':')
    rss_array = arr0[5].split(':')
    time_array = arr0[1].split('][')
    if len(cpu_array) < 2 or len(rss_array) < 2 or len(time_array) < 2:
        print(line)
        return ret_d

    ret_d['time'] = time_array[0]
    ret_d['cpu'] = cpu_array[1].strip('%')
    ret_d['rss'] = int(rss_array[1].strip('K'))
    return ret_d

class DataFormat:
    #输入数据格式化
    def __init__(self, filename="./mem.txt"):
        self.file_path = filename
        if not os.path.exists(self.file_path):
            print(self.file_path + "is not exist")
            exit(0)

    def _data_append(self, dst, src):
        for key in src:
            if type(src[key]) is not dict:
                if key not in dst:
                    dst[key] = list()
                dst[key].append(src[key])
                #print(key, " len is ", len(dst[key]))
            else:
                if key not in dst:
                    dst[key] = dict()
                self._data_append(dst[key], src[key])
                    
    def _file_read(self):
        fp = open(self.file_path, "r", errors='ignore', encoding='utf-8')
        line = fp.readline()
        self.data = dict()
        while line is not None:
            ret = self.data_filter(line)
            self._data_append(dst=self.data, src=ret)

            line = fp.readline()
            if not line:
                print("file end")
                for key in self.data:
                    if key.find('mixpad_gui') != -1 or key.find('ember-host') != -1:
                        print(key, self.data[key])
                        print(len(self.data[key]))
                    #print(key, len(self.data[key]))
                break


    def data_filter(self, line):
        m_dict = {'.*\[monitor INFO\].*vispeech\[.*': orb_log_cbk,
                'Mem:.*': Mem_cbk,
                'CPU:.*': CPU_cbk,
                'datestamp.*': datestamp_cbk,
                'timestamp.*': timestamp_cbk,
                '.*:VmRSS=.*;VmData.*': VmRSS_VmData_cbk}
        ret_d = dict()
        for key in m_dict:
            matchLine = re.search(key, line)
            if matchLine is not None:
                ret_d = m_dict[key](line)
        return ret_d

    def run(self):
        self._file_read()


class DataDraw:
    #格式化数据可视化
    fig_type = {'time': 1, 'datestamp': 2} #根据数据中的关键词区分图形显示样式
    cpu_keys = ['usr','sys','nic','idle','io','irq','sirq']
    mem_keys = ['used','free','shrd','buff','cached']
    proc_keys = ["vispeech","vifamily","mixpad_gui","system_manager","vicenter","audio_manager","guiservice","mixpad_music","ember-host","dbus-daemon"]
    hide_keys = ['nic','idle','irq','sirq','usr','sys', 'VmData','\/oem\/ember-host\/bin\/ember-host']
    def __init__(self, data):
        self.data = data
        self.type = self.figure_type_check(data)
        self.fig = plt.figure()
        if self.type == 1:
            self.cpu_figure = self.fig.add_subplot(2, 1, 1)
            self.rss_figure = self.fig.add_subplot(2, 1, 2)
        elif self.type == 2:
            self.cpu_figure = self.fig.add_subplot(3, 1, 2)
            self.mem_figure = self.fig.add_subplot(3, 1, 1)
            self.proc_figure = self.fig.add_subplot(3, 1, 3)

    def list_align(self, l0, l1):
        len0 = len(l0)
        len1 = len(l1)
        #print(len0,":", len1)
        #print(l0, l1)
        while len(l0) > len1:
            l0.pop()
        while len(l1) > len0:
            l1.pop()
 
    def figure_type_check(self, data):
        for key in data:
            if key in self.fig_type:
                return self.fig_type[key]

    def run(self):
        color_array = ["aliceblue", "black", "blue", "brown", "coral", "tomato", "pink", "yellow", "green", "red", "gray", "cyan", "darkgreen", "darkgray", "burlywood"]
        
        i_cpu = 0
        i_mem = 0
        i_proc = 0
        for key in self.data:
            print(key)
            if key in self.hide_keys:
                #隐藏的数据不显示线条
                continue

            if self.type == 1 and key == 'time':
                continue
            elif self.type == 2 and key == 'datestamp':
                continue
            if type(self.data[key]) is list:
                if self.type == 1:
                    i_cpu = i_cpu + 1
                    self.list_align(l0=self.data['time'], l1=self.data[key])
                    if key == 'cpu':
                        self.cpu_figure.plot(self.data['time'], self.data[key], label = key, color = color_array[i_cpu])
                    elif key == 'rss':
                        self.rss_figure.plot(self.data['time'], self.data[key], label = key, color = color_array[i_cpu])
                elif self.type == 2:
                    if key in self.cpu_keys:
                        i_cpu = i_cpu + 1
                        self.cpu_figure.plot(self.data[key], label = key, color = color_array[i_cpu])
                    elif key in self.mem_keys:
                        i_mem = i_mem + 1
                        self.mem_figure.plot(self.data[key], label = key, color = color_array[i_mem])
                    elif key in self.proc_keys:
                        i_proc = i_proc + 1
                        self.proc_figure.plot(self.data[key], label = key, color = color_array[i_proc])
            elif type(self.data[key]) is dict:
                i_proc = i_proc + 1
                for k in self.data[key]:
                    if k in self.hide_keys:
                        #隐藏的数据不显示线条
                        continue
                    self.list_align(l0=self.data['datestamp'], l1=self.data[key][k])
                    self.proc_figure.plot(self.data['datestamp'], self.data[key][k], label = key + "." + k, color = color_array[i_proc])
            #self.a1.plot(self.data['time'], self.data[key], label = key, color = color_array[i])

        if self.type == 1:
            self.cpu_figure.legend()
            self.rss_figure.legend()
            x_major_locator=LinearLocator(15)
            y_major_locator=LinearLocator(10)
            self.cpu_figure.yaxis.set_major_locator(y_major_locator)
            self.rss_figure.xaxis.set_major_locator(x_major_locator)
        elif self.type == 2:
            self.proc_figure.legend()
            self.cpu_figure.legend()
            self.mem_figure.legend()
            self.proc_figure.grid()
            #x_major_locator=MultipleLocator(180)
            #y_major_locator=MultipleLocator(5000)
            x_major_locator=LinearLocator(20)
            y_major_locator=LinearLocator(10)
            self.proc_figure.yaxis.set_major_locator(y_major_locator)
            self.proc_figure.xaxis.set_major_locator(x_major_locator)
            #plt.ylim(100, 220000)

        plt.show()


if __name__=="__main__":
    print("start............")
    df = DataFormat(sys.argv[1])
    df.run()
    dd = DataDraw(df.data)
    dd.run()
    print("end............")
    exit()
