#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: minx@amd.com
# based on the Python3
# support FIO 3.x
# validate on the libaio ioengine

import os
import re
import sys
import time
import datetime
import math
import argparse
from itertools import chain
from multiprocessing import Pool, Lock, Value
# import ConfigParser
import configparser  # for py3
from tempfile import NamedTemporaryFile
import json

import logging
import subprocess
from tabulate import tabulate

import psutil
import cpuinfo

from pandas import DataFrame

import warnings

warnings.filterwarnings('ignore')

logging.basicConfig(filename='/tmp/xnvmebench.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)
logging.info('log begin.')


#fio conf path,

PWD=os.path.abspath(os.curdir)
PATH=PWD
RUN_PATH='/tmp/xnvme/conf'

time_stamp = time.strftime("%Y_%m_%d-%H_%M_%S", time.localtime()) 
FIO_RESULT_PATH = 'data'
DATA_PATH='data_' + time_stamp

LOG_PATH='log'
BW_LOG_PATH = './bwlog_' + time_stamp
IOPS_LOG_PATH = './iopslog_' + time_stamp
LAT_LOG_PATH = './latlog_' + time_stamp

def list_fio_pattern():

    try:
        files= os.listdir(PATH)
        for each_file in files:
            print (each_file)
            
    except Exception as e:
        print ("e")


def print_fio_pattern(test_type,job_id):
    file='{}/{}'.format(PATH,job_id)

    try:
        with open(file,'r') as f:
            data=f.read()

        title='    #### {} ####'.format(job_id)
        print (title)
        print (data)

    except Exception as e:
        print (e)

def run_fio_conf(job_id=None,filename=None,fio_size=None,fio_runtime=None):
    
    # todo check the output return
    output=subprocess.getoutput("mkdir -p {}".format(RUN_PATH))

    output=subprocess.getoutput("cp -r {}/{} {}".format(PATH,job_id,RUN_PATH))

    # output=subprocess.getoutput("mkdir -p {}".format(IOPS_LOG_PATH))
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)

    if not os.path.exists(FIO_RESULT_PATH):
        os.makedirs(FIO_RESULT_PATH)

    if not os.path.exists(FIO_RESULT_PATH +'/'+ DATA_PATH):
        os.makedirs(FIO_RESULT_PATH +'/'+ DATA_PATH)

    file='{}/{}'.format(RUN_PATH,job_id)
    # print(file)

    try:
        with open(file,'r') as f:
            lines=f.readlines()

        for index,item in enumerate(lines):
            if "write_iops_log" in item:
                if not os.path.exists(LOG_PATH+'/'+IOPS_LOG_PATH):
                    os.makedirs(LOG_PATH+'/'+IOPS_LOG_PATH)

        for index,item in enumerate(lines):
            if "write_bw_log" in item:
                if not os.path.exists(LOG_PATH+'/'+BW_LOG_PATH):
                    os.makedirs(LOG_PATH+'/'+BW_LOG_PATH)

        for index,item in enumerate(lines):
            if "write_lat_log" in item:
                if not os.path.exists(LOG_PATH+'/'+LAT_LOG_PATH):
                    os.makedirs(LOG_PATH+'/'+LAT_LOG_PATH)

        if filename != None or fio_size != None or fio_runtime != None:
            for index,item in enumerate(lines):
                if filename != None:
                    if 'filename=' in item:
                        lines[index]='filename={}\n'.format(filename)
                if fio_size != None:
                    if 'size' in item:
                        lines[index]='size={}\n'.format(fio_size)
                if fio_runtime != None:
                    if 'runtime' in item:
                        lines[index]='runtime={}\n'.format(fio_runtime)
        
        for index,item in enumerate(lines):
            if 'write_iops_log=' in item:
                #目录拼接
                # print (IOPS_LOG_PATH+'/'+lines[index].split('=')[1])
                lines[index] = 'write_iops_log={}\n'.format(LOG_PATH+'/'+IOPS_LOG_PATH+'/'+lines[index].split('=')[1])

        for index,item in enumerate(lines):
            if 'write_bw_log=' in item:
                #目录拼接
                # print (BW_LOG_PATH+'/'+lines[index].split('=')[1])
                lines[index] = 'write_bw_log={}\n'.format(LOG_PATH+'/'+BW_LOG_PATH+'/'+lines[index].split('=')[1])
        
        for index,item in enumerate(lines):
            if 'write_lat_log=' in item:
                #目录拼接
                # print (LAT_LOG_PATH+'/'+lines[index].split('=')[1])
                lines[index] = 'write_lat_log={}\n'.format(LOG_PATH+'/'+LAT_LOG_PATH+'/'+lines[index].split('=')[1])
                


        with open(file,'w') as f:
            f.writelines(lines)
        #print "patch fio conf ok: {}".format(file)
    except Exception as e:
        print ('counter exception: {}'.format(str(e)))

    # # fio conf is not totally ini conf,--groupreporting for example
    # try:
    #     cf = configparser.SafeConfigParser()
    #     cf.read(file)
    #     secs = cf.sections() 
    #     print (secs)
    # except Exception as e:
    #     print ('configparser exception: {}'.format(str(e)))

def get_fio_conf_jobs(job_id=None):

    conf_job_cnt = 0

    file='{}/{}'.format(RUN_PATH,job_id)

    try:
        with open(file,'r') as f:
            lines=f.readlines()
        #print 'befor patch ,the conf is {}'.format(lines)

        for index,item in enumerate(lines):
            if '[' in item:
                conf_job_cnt = conf_job_cnt + 1
    except Exception as e:
        print ('counter exception: {}'.format(str(e)))
    return conf_job_cnt




def get_fio_version():
    output=subprocess.getoutput("fio -v")
    if 'fio-3.' in output:
        return 'version3'
    else:
        return 'other'

def do_fio_job(job_id,filename=None,fio_size=None,fio_runtime=None):

    run_fio_conf(job_id,filename,fio_size,fio_runtime)
    run_conf='{}/{}'.format(RUN_PATH,job_id)
    # todo 打印开始时间
    try:
        # output=subprocess.getoutput("fio {}".format(run_conf))
        # print(output)
        # print ("start in {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        output=subprocess.getoutput("date")
        print(output)
        start = time.time()
        output=subprocess.getoutput("fio {} --output-format=json".format(run_conf))
        end = time.time()
        print("========= fio spend {} mins=======".format(float(end-start)/float(60.00)))
        data=json.loads(output)

        # format data
        logging.info('have complete fio job :{}.'.format(run_conf))
        logging.info('fio result is :{}.'.format(json.dumps(data)))
    
        fio_version=get_fio_version()
        # print ("check the fio version: {}".format(fio_version))

        if fio_version == 'version3':
            fio_3x_result_format(data,job_id)
        else:
            print ('fio version is not expected')
            exit(-1)
    except Exception as e:
        # print(output)
        print(data)
        print ('do_fio_job exception: {}'.format(str(e)))
         



def print_header(header):
    # print ('\n')
    print ('=========  result of {}  =========      '.format(header))
    #print '------------------------------------------------------------------'
    #print 'type               |iops              |bandwidth                  '
    #print '------------------------------------------------------------------'


def fio_3x_result_format(data,job_id):

    conf_job_cnt = get_fio_conf_jobs(job_id)
    conf_job_cnt = conf_job_cnt -1  # 去掉global 的配置
    # print("conf_job_cnt: {}".format(conf_job_cnt))

    time = data['time']
    print("========= run time: {}=======".format(time))

    result = []
    result_sum = []

    numjobs_offset = 0

    if 'group_reporting' in data['global options'].keys():
        # print("group reporting")
        
        rw_type = data['jobs'][0]['job options']['rw']

        if rw_type == 'read' or rw_type == 'randread':
            result.append(data['jobs'][0]['job options']['rw'])
            result.append(data['jobs'][0]['read']['iops']/1000)
            result.append(data['jobs'][0]['read']['bw']/1024)
            result.append(data['jobs'][0]['read']['lat_ns']['mean']/1000)
            result.append(data['jobs'][0]['read']['clat_ns']["percentile"]["90.000000"]/1000)
            result.append(data['jobs'][0]['read']['clat_ns']["percentile"]["95.000000"]/1000)
            result.append(data['jobs'][0]['read']['clat_ns']["percentile"]["99.000000"]/1000)
            result.append(data['jobs'][0]['read']['clat_ns']["percentile"]["99.900000"]/1000)

            if 'iodepth' in data['jobs'][0]['job options'].keys():
                result.append(data['jobs'][0]['job options']['iodepth'])
            elif 'iodepth' in data['global options'].keys():
                result.append(data['global options']['iodepth'])
            else:
                result.append("")

            if 'bs' in data['jobs'][0]['job options'].keys():
                # print(data['jobs'][int(job)+int(thread)]['job options']['bs'])
                result.append(data['jobs'][0]['job options']['bs'])
            elif 'bs' in data['global options'].keys():
                result.append(data['global options']['bs'])
            else:
                result.append("")

            result.append(data['jobs'][0]['job options']['filename'])

            if 'numjobs' in data['jobs'][0]['job options'].keys():
                result.append(data['jobs'][0]['job options']['numjobs']+ ' threads')
            elif 'numjobs' in data['global options'].keys():
                result.append(data['global options']['numjobs'] +' threads')
            else:
                result.append("1")

        elif rw_type == 'write' or rw_type == 'randwrite':
            # print("write")
            result.append(data['jobs'][0]['job options']['rw'])
            result.append(data['jobs'][0]['write']['iops']/1000)
            result.append(data['jobs'][0]['write']['bw']/1024)
            result.append(data['jobs'][0]['write']['lat_ns']['mean']/1000)
            result.append(data['jobs'][0]['write']['clat_ns']["percentile"]["90.000000"]/1000)
            result.append(data['jobs'][0]['write']['clat_ns']["percentile"]["95.000000"]/1000)
            result.append(data['jobs'][0]['write']['clat_ns']["percentile"]["99.000000"]/1000)
            result.append(data['jobs'][0]['write']['clat_ns']["percentile"]["99.900000"]/1000)
   
            if 'iodepth' in data['jobs'][0]['job options'].keys():
                # print('get iodepth')
                # print(data['jobs'][0]['job options']['iodepth'])
                result.append(data['jobs'][0]['job options']['iodepth'])
            elif 'iodepth' in data['global options'].keys():
                result.append(data['global options']['iodepth'])
            else:
                result.append("")

            if 'bs' in data['jobs'][0]['job options'].keys():
                # print(data['jobs'][0]['job options']['bs'])
                result.append(data['jobs'][0]['job options']['bs'])
            elif 'bs' in data['global options'].keys():
                result.append(data['global options']['bs'])
            else:
                result.append("")

            result.append(data['jobs'][0]['job options']['filename'])

            if 'numjobs' in data['jobs'][0]['job options'].keys():
                result.append(data['jobs'][0]['job options']['numjobs']+ ' threads')
            elif 'numjobs' in data['global options'].keys():
                result.append(data['global options']['numjobs'] +' threads')
            else:
                result.append("1")

        elif rw_type == 'rw' or rw_type == 'randrw':
            # print('randrw')
            if data['jobs'][0]['job options']['rw'] == 'randrw':
                result.append('rw-randread')
            else:
                result.append('rw-read')

            result.append(data['jobs'][0]['read']['iops']/1000)
            result.append(data['jobs'][0]['read']['bw']/1024)
            result.append(data['jobs'][0]['read']['lat_ns']['mean']/1000)
            result.append(data['jobs'][0]['read']['clat_ns']["percentile"]["90.000000"]/1000)
            result.append(data['jobs'][0]['read']['clat_ns']["percentile"]["95.000000"]/1000)
            result.append(data['jobs'][0]['read']['clat_ns']["percentile"]["99.000000"]/1000)
            result.append(data['jobs'][0]['read']['clat_ns']["percentile"]["99.900000"]/1000)

            if 'iodepth' in data['jobs'][0]['job options'].keys():
                # print(data['jobs'][int(job)+int(thread)]['job options']['iodepth'])
                result.append(data['jobs'][0]['job options']['iodepth'])
            elif 'iodepth' in data['global options'].keys():
                result.append(data['global options']['iodepth'])
            else:
                result.append("")

            if 'bs' in data['jobs'][0]['job options'].keys():
                # print(data['jobs'][int(job)+int(thread)]['job options']['bs'])
                result.append(data['jobs'][0]['job options']['bs'])
            elif 'bs' in data['global options'].keys():
                result.append(data['global options']['bs'])
            else:
                result.append("")

            result.append(data['jobs'][0]['job options']['filename'])

            if 'numjobs' in data['jobs'][0]['job options'].keys():
                result.append(data['jobs'][0]['job options']['numjobs']+ ' threads')
            elif 'numjobs' in data['global options'].keys():
                result.append(data['global options']['numjobs'] +' threads')
            else:
                result.append("1")

            result_sum.append(result)
            result = []

            if data['jobs'][0]['job options']['rw'] == 'randrw':
                result.append('rw-randwrite')
            else:
                result.append('rw-write')
            # result.append(data['jobs'][int(job)+int(thread)]['job options']['rw']+'_'+str(job)+'_'+str(thread))
            result.append(data['jobs'][0]['write']['iops']/1000)
            result.append(data['jobs'][0]['write']['bw']/1024)
            result.append(data['jobs'][0]['write']['lat_ns']['mean']/1000)
            result.append(data['jobs'][0]['write']['clat_ns']["percentile"]["90.000000"]/1000)
            result.append(data['jobs'][0]['write']['clat_ns']["percentile"]["95.000000"]/1000)
            result.append(data['jobs'][0]['write']['clat_ns']["percentile"]["99.000000"]/1000)
            result.append(data['jobs'][0]['write']['clat_ns']["percentile"]["99.900000"]/1000)

            
            if 'iodepth' in data['jobs'][0]['job options'].keys():
                # print('get iodepth')
                # print(data['jobs'][0]['job options']['iodepth'])
                result.append(data['jobs'][0]['job options']['iodepth'])
            elif 'iodepth' in data['global options'].keys():
                result.append(data['global options']['iodepth'])
            else:
                result.append("")

            if 'bs' in data['jobs'][0]['job options'].keys():
                print(data['jobs'][0]['job options']['bs'])
                result.append(data['jobs'][0]['job options']['bs'])
            elif 'bs' in data['global options'].keys():
                result.append(data['global options']['bs'])
            else:
                result.append("")

            result.append(data['jobs'][0]['job options']['filename'])

            if 'numjobs' in data['jobs'][0]['job options'].keys():
                result.append(data['jobs'][0]['job options']['numjobs']+ ' threads')
            elif 'numjobs' in data['global options'].keys():
                result.append(data['global options']['numjobs'] +' threads')
            else:
                result.append("1")

        else:
            print("does not match")

        result_sum.append(result)
        result = []
    else:
        conf_job_cnt = get_fio_conf_jobs(job_id)
        conf_job_cnt = conf_job_cnt -1  # 去掉global 的配置
        # print("conf_job_cnt: {}".format(conf_job_cnt))

        for job in range(0, conf_job_cnt):
            # print("job{}".format(job))
            # 每个conf_job 提取本次的numjobs, 用于下一次conf_job的偏移
            if 'numjobs' in data['jobs'][int(numjobs_offset)]['job options'].keys():
                numjobs = data['jobs'][int(numjobs_offset)]['job options']['numjobs']
            else:
                numjobs = 1
            # print("numjobs : {}".format(numjobs))
            numjobs_offset = numjobs_offset + int(numjobs)
            # print("numjobs_offset", numjobs_offset)

            # 读取每个conf_job 的numjobs 的最后一个
            rw_type = data['jobs'][int(numjobs_offset)-1]['job options']['rw']
        
            for thread in range(0, int(numjobs)):
                if rw_type == 'read' or rw_type == 'randread':
                    result.append(data['jobs'][int(job)+int(thread)]['job options']['rw']+'_'+str(job)+'_'+str(thread))
                    result.append(data['jobs'][int(job)+int(thread)]['read']['iops']/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['read']['bw']/1024)
                    result.append(data['jobs'][int(job)+int(thread)]['read']['lat_ns']['mean']/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['read']['clat_ns']["percentile"]["90.000000"]/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['read']['clat_ns']["percentile"]["95.000000"]/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['read']['clat_ns']["percentile"]["99.000000"]/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['read']['clat_ns']["percentile"]["99.900000"]/1000)

                    if 'iodepth' in data['jobs'][int(job)+int(thread)]['job options'].keys():
                        # print(data['jobs'][int(job)+int(thread)]['job options']['iodepth'])
                        result.append(data['jobs'][int(job)+int(thread)]['job options']['iodepth'])
                    elif 'iodepth' in data['global options'].keys():
                        result.append(data['global options']['iodepth'])
                    else:
                        result.append("")

                    if 'bs' in data['jobs'][int(job)+int(thread)]['job options'].keys():
                        # print(data['jobs'][int(job)+int(thread)]['job options']['bs'])
                        result.append(data['jobs'][int(job)+int(thread)]['job options']['bs'])
                    elif 'bs' in data['global options'].keys():
                        result.append(data['global options']['bs'])
                    else:
                        result.append("")

                    result.append(data['jobs'][int(job)+int(thread)]['job options']['filename'])

                elif rw_type == 'write' or rw_type == 'randwrite':
                    # result.append(rw_type +job+'_'+thread))
                    result.append(data['jobs'][int(job)+int(thread)]['job options']['rw']+'_'+str(job)+'_'+str(thread))
                    result.append(data['jobs'][int(job)+int(thread)]['write']['iops']/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['write']['bw']/1024)
                    result.append(data['jobs'][int(job)+int(thread)]['write']['lat_ns']['mean']/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['write']['clat_ns']["percentile"]["90.000000"]/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['write']['clat_ns']["percentile"]["95.000000"]/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['write']['clat_ns']["percentile"]["99.000000"]/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['write']['clat_ns']["percentile"]["99.900000"]/1000)

                    
                    if 'iodepth' in data['jobs'][int(job)+int(thread)]['job options'].keys():
                        # print('get iodepth')
                        # print(data['jobs'][int(job)+int(thread)]['job options']['iodepth'])
                        result.append(data['jobs'][int(job)+int(thread)]['job options']['iodepth'])
                    elif 'iodepth' in data['global options'].keys():
                        result.append(data['global options']['iodepth'])
                    else:
                        result.append("")

                    if 'bs' in data['jobs'][int(job)+int(thread)]['job options'].keys():
                        print(data['jobs'][int(job)+int(thread)]['job options']['bs'])
                        result.append(data['jobs'][int(job)+int(thread)]['job options']['bs'])
                    elif 'bs' in data['global options'].keys():
                        result.append(data['global options']['bs'])
                    else:
                        result.append("")
                    result.append(data['jobs'][int(job)+int(thread)]['job options']['filename'])


                elif rw_type == 'rw' or rw_type == 'randrw':
                    # result.append(data['jobs'][int(job)+int(thread)]['job options']['rw']+'_'+str(job)+'_'+str(thread))
                    if data['jobs'][int(job)+int(thread)]['job options']['rw'] == 'randrw':
                        result.append('randread'+'_'+str(job)+'_'+str(thread))
                    else:
                        result.append('read'+'_'+str(job)+'_'+str(thread))

                    result.append(data['jobs'][int(job)+int(thread)]['read']['iops']/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['read']['bw']/1024)
                    result.append(data['jobs'][int(job)+int(thread)]['read']['lat_ns']['mean']/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['read']['clat_ns']["percentile"]["90.000000"]/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['read']['clat_ns']["percentile"]["95.000000"]/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['read']['clat_ns']["percentile"]["99.000000"]/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['read']['clat_ns']["percentile"]["99.900000"]/1000)

                    if 'iodepth' in data['jobs'][int(job)+int(thread)]['job options'].keys():
                        # print(data['jobs'][int(job)+int(thread)]['job options']['iodepth'])
                        result.append(data['jobs'][int(job)+int(thread)]['job options']['iodepth'])
                    elif 'iodepth' in data['global options'].keys():
                        result.append(data['global options']['iodepth'])
                    else:
                        result.append("")

                    if 'bs' in data['jobs'][int(job)+int(thread)]['job options'].keys():
                        # print(data['jobs'][int(job)+int(thread)]['job options']['bs'])
                        result.append(data['jobs'][int(job)+int(thread)]['job options']['bs'])
                    elif 'bs' in data['global options'].keys():
                        result.append(data['global options']['bs'])
                    else:
                        result.append("")

                    result.append(data['jobs'][int(job)+int(thread)]['job options']['filename'])

                    result_sum.append(result)
                    result = []

                    if data['jobs'][int(job)+int(thread)]['job options']['rw'] == 'randrw':
                        result.append('randwrite'+'_'+str(job)+'_'+str(thread))
                    else:
                        result.append('write'+'_'+str(job)+'_'+str(thread))

                    # result.append(data['jobs'][int(job)+int(thread)]['job options']['rw']+'_'+str(job)+'_'+str(thread))
                    result.append(data['jobs'][int(job)+int(thread)]['write']['iops']/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['write']['bw']/1024)
                    result.append(data['jobs'][int(job)+int(thread)]['write']['lat_ns']['mean']/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['write']['clat_ns']["percentile"]["90.000000"]/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['write']['clat_ns']["percentile"]["95.000000"]/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['write']['clat_ns']["percentile"]["99.000000"]/1000)
                    result.append(data['jobs'][int(job)+int(thread)]['write']['clat_ns']["percentile"]["99.900000"]/1000)

                    
                    if 'iodepth' in data['jobs'][int(job)+int(thread)]['job options'].keys():
                        # print('get iodepth')
                        # print(data['jobs'][int(job)+int(thread)]['job options']['iodepth'])
                        result.append(data['jobs'][int(job)+int(thread)]['job options']['iodepth'])
                    elif 'iodepth' in data['global options'].keys():
                        result.append(data['global options']['iodepth'])
                    else:
                        result.append("")

                    if 'bs' in data['jobs'][int(job)+int(thread)]['job options'].keys():
                        print(data['jobs'][int(job)+int(thread)]['job options']['bs'])
                        result.append(data['jobs'][int(job)+int(thread)]['job options']['bs'])
                    elif 'bs' in data['global options'].keys():
                        result.append(data['global options']['bs'])
                    else:
                        result.append("")
                    result.append(data['jobs'][int(job)+int(thread)]['job options']['filename'])

                else:
                    print("does not match")
                
                result_sum.append(result)
                result = []

    print_header(job_id)

    # print(result_sum)

    #excel 表头
    if 'group_reporting' in data['global options'].keys():
        columns_head = ['type', 'iops(k)','bandwidth(MB)','latency_avg(us)','latency_90%','latency_95%','latency_99%','latency_99.9%','iodepth','blk size', 'device','group']
    else:
        columns_head = ['type', 'iops(k)','bandwidth(MB)','latency_avg(us)','latency_90%','latency_95%','latency_99%','latency_99.9%','iodepth','blk size', 'device']

    df = DataFrame(data = result_sum, columns = columns_head)
    # DATA_PATH
    df.to_excel(FIO_RESULT_PATH+'/'+DATA_PATH+'/'+job_id+data['time']+'.xlsx', sheet_name=job_id, index=False)

    print(tabulate(result_sum, headers=columns_head, tablefmt='orgtbl'))
    
   
    #print result
def do_all_fio_jobs(fio_filename,fio_size,fio_runtime):
     try:
         files= os.listdir(PATH)
         for each_file in files:
             do_fio_job(each_file,fio_filename,fio_size,fio_runtime)
     except Exception as e:
         print ('counter exception: {}'.format(str(e)))

def do_group_fio_jobs(group_path, fio_runtime=None):
     try:
        files= os.listdir(group_path)
        if fio_runtime != None:
            for each_file in files:
                do_fio_job(each_file, fio_runtime=fio_runtime)
        else:
            for each_file in files:
                do_fio_job(each_file)
     except Exception as e:
         print ('counter exception: {}'.format(str(e)))


def main():
    parser = argparse.ArgumentParser(
        description='xnvme fio bench')
    parser.add_argument('-r','--type', action="store_true",default='nvme',help='info')
    parser.add_argument('-l','--listjobs', action="store_true",help='destination of jobs, cannot be empty')
    parser.add_argument('-p','--printjobs', action="store_true",help='print job')
    parser.add_argument('-j','--job_id',help='job id')
    parser.add_argument('-g','--group_id',help='group id， cannot be empty')
    parser.add_argument('-t','--runtime_of_each_job',help='run time of each job')
    parser.add_argument('-d','--destination',
                        help='filename parameter in fio, for NVME it is a device like /dev/nvme0n1')
    parser.add_argument('-s','--size',help='size parameter in fio,like 100M or 10G or 1T')


    options = parser.parse_args()

    if options.listjobs:
        print ('list jobs')
        list_fio_pattern()

    if options.printjobs:
        print ('print jobs')
        if not options.job_id:
            print ("plesase spcify the job id")
        else:
            print (options.type)
            print_fio_pattern(options.type,options.job_id)

    if options.job_id and options.destination and options.size and options.runtime_of_each_job:
        do_fio_job(options.job_id,options.destination,options.size,options.runtime_of_each_job)
    
    if options.job_id:
        if not options.runtime_of_each_job and not options.destination:
            print("开始执行用例{}".format(options.job_id))
            do_fio_job(options.job_id)

    # do_fio_job(job_id,filename=None,fio_size=None,fio_runtime=None):
    if options.job_id and options.destination:
        print("开始执行用例{}，指定NVME盘{}".format(options.job_id,options.destination))
        do_fio_job(options.job_id, filename=options.destination)
        return 
        
    if options.job_id and options.runtime_of_each_job:
        print("开始执行用例{}，设置运行{}秒".format(options.job_id, options.runtime_of_each_job))
        do_fio_job(options.job_id, fio_runtime=options.runtime_of_each_job)
        return

    if options.group_id:
        if not options.runtime_of_each_job:
            print("开始执行用例组{}".format(options.group_id))
            print(options.group_id)
            do_group_fio_jobs(options.group_id)
            return

    if options.group_id and options.runtime_of_each_job:
        print("开始执行用例组{} 设置每个用例运行{}秒".format(options.group_id, options.runtime_of_each_job))
        print(options.group_id)
        do_group_fio_jobs(options.group_id,options.runtime_of_each_job)
        return

    if  options.destination and options.size and options.runtime_of_each_job:
        if not options.job_id:
            do_all_fio_jobs(options.destination,options.size,options.runtime_of_each_job)

def get_system_info():

    try:
        cpu = cpuinfo.get_cpu_info()
        print("CPU:  {} {} {}bit {}core {}Hz".format(cpu['brand_raw'],cpu['arch'], cpu['bits'], cpu['count'], cpu['hz_actual'][0]))
        mem = psutil.virtual_memory()
        print("内存: {}G".format(mem.total/1024/1024/1024))

        print("系统： {}".format(subprocess.getoutput("uname -a")))
        print("工具： {}".format(subprocess.getoutput("fio -v")))

    except Exception as e:
         print("Get system info fail")
        #  print ('counter exception: {}'.format(str(e)))

if __name__ == '__main__':

    if os.geteuid() != 0:
        print ("Access the nvme disk must be run as root. Aborting.")
        sys.exit(1)
    else:
        get_system_info()
        main()
        print("####   Complete   ####")
        print("\n")
        sys.exit(0)
