#!/usr/bin/python3
# coding: utf-8

import sys
import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl


mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'NSimSun,Times New Roman'

colors = ['red','black','green','blue','purple','orange','magenta','cyan','pink','gray','brown','olive', 'chocolate', 'cornflowerblue', 'darkorchid', 'goldenrod', 'rosybrown','skyblue']
# labels = ['xnvme', 'p5510']

# a = np.loadtxt('./bwlog_fioa_seq_wtire_bs128k_iodep128_job1_bw.1.log', delimiter=',')
# print(a)

def main():

    parser = argparse.ArgumentParser(description='xnvme fio bench plot tool')

    parser.add_argument('-f','--file',action='append', help='bw/iops/latency file')
    parser.add_argument('-l','--lable',action='append', help='lable')
    parser.add_argument('-t','--type',help='file log type bw/io/la')

    options = parser.parse_args()

    if options.file and options.type  and options.lable:
        files = options.file
        labels = options.lable
        type = options.type
    else:
        print("please input a bw/iops/latancy log file and file type")
        exit(-1)

    # check the type
    if type not in ['bw', 'io', 'la']:
        print("input type shoud be bw-bandwidth, io-iops or la-latency")
        exit(0)

    
    i = 0
    fig, ax = plt.subplots() 
    
    for file in files:
        # to do check if file exist
        if os.path.isfile(file):
            x,y,z,v = np.loadtxt(str(file), delimiter=',', unpack=True)
            ax.plot(x, y, '.', label=labels[i], color=colors[i])
            i=i+1
            # plt.plot(x,y)
        else:
            print("the input file {} does not exist".format(file))
            exit(-1)

    title = os.path.basename(files[0])
    title = title.split(".")[0]
    print(title)
    ax.set_xlabel('time_ms')

    if type == 'bw':
        ax.set_ylabel('throughput_mb')
        ax.set_title(title +' throughput-time grapth')
    elif type == 'io':
        ax.set_ylabel('iops')
        ax.set_title(title +' grapth')
    elif type == 'la':
        ax.set_ylabel('latency')
        ax.set_title(title +'latency-time grapth')
    else:
        ax.set_ylabel('throughput_mb')
        ax.set_title(title +' throughput-time grapth')

    ax.legend()

    
    #plt.show()
    #plt.legend()
    # plt.show()
    # plt.savefig(path.join('.jpg'))
    if len(files) == 1:
        title=os.path.basename(files[0])
    else:
        title = os.path.basename(files[0])
        title = title.split(".")[0]
    # print(title)
    plt.savefig(title+'.jpg')
    plt.clf () #清除当前图形及其所有轴，但保持窗口打开，以便可以将其重新用于其他绘图。
    plt.close () 

if __name__ == '__main__':
    main()
    sys.exit(0)