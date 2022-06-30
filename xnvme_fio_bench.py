#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
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


logging.basicConfig(filename='/tmp/xnvmebench.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S',level=logging.INFO)
logging.info('log begin.')


#fio conf path,

PWD=os.path.abspath(os.curdir)
PATH=PWD
RUN_PATH='/tmp/xnvme/conf'


def list_fio_pattern():
    try:
        files= os.listdir(PATH)
        for each_file in files:
            print (each_file)
    except Exception as e:
        print ("some erro")


def print_fio_pattern(test_type,job_id):
    file='{}/{}'.format(PATH,job_id)

    try:
        with open(file,'r') as f:
            data=f.read()

        title='    #### {} ####'.format(job_id)
        print (title)
        print (data)

    except Exception as e:
        print ("some erro")

def run_fio_conf(job_id=None,filename=None,fio_size=None,fio_runtime=None):
    
    output=subprocess.getoutput("mkdir -p {}".format(RUN_PATH))
    output=subprocess.getoutput("cp -r {}/{} {}".format(PATH,job_id,RUN_PATH))

    file='{}/{}'.format(RUN_PATH,job_id)
    print(file)

    try:
        with open(file,'r') as f:
            lines=f.readlines()
        #print 'befor patch ,the conf is {}'.format(lines)
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
    try:
        output=subprocess.getoutput("fio {} --output-format=json".format(run_conf))
        data=json.loads(output)

        # format data
        logging.info('have complete fio job :{}.'.format(run_conf))
        logging.info('fio result is :{}.'.format(json.dumps(data)))
    
        fio_version=get_fio_version()
        print ("check the fio version: {}".format(fio_version))

        if fio_version == 'version3':
            fio_3x_result_format(data,job_id)
        else:
            print ('fio version is not expected')
    except Exception as e:
         print ('do_fio_job exception: {}'.format(str(e)))



def print_header(header):
    print ('\n')
    print ('=========  result of {}  =========      '.format(header))
    #print '------------------------------------------------------------------'
    #print 'type               |iops              |bandwidth                  '
    #print '------------------------------------------------------------------'


def fio_3x_result_format(data,job_id):
    # result={}
    # result['type']=''

    # print(data)
    # print(data['global options'])
    conf_job_cnt = get_fio_conf_jobs(job_id)
    conf_job_cnt = conf_job_cnt -1  # 去掉global 的配置
    print("conf_job_cnt: {}".format(conf_job_cnt))

    time = data['time']
    print("test time: {}".format(time))

    result = []
    result_sum = []

    numjobs_offset = 0

    for job in range(0, conf_job_cnt):

        print("job{}".format(job))

        # 每个conf_job 提取本次的numjobs, 用于下一次conf_job的偏移
        if 'numjobs' in data['jobs'][int(numjobs_offset)]['job options'].keys():
            numjobs = data['jobs'][int(numjobs_offset)]['job options']['numjobs']
        else:
            numjobs = 1
        print("numjobs : {}".format(numjobs))
        numjobs_offset = numjobs_offset + int(numjobs)
        print("numjobs_offset", numjobs_offset)

        # 读取每个conf_job 的numjobs 的最后一个
        rw_type = data['jobs'][int(numjobs_offset)-1]['job options']['rw']
       

        for thread in range(0, int(numjobs)):
            if rw_type == 'read' or rw_type == 'randread':

                result.append(data['jobs'][int(job)+int(thread)]['job options']['rw'])
                result.append(data['jobs'][int(job)+int(thread)]['read']['iops'])
                result.append(data['jobs'][int(job)+int(thread)]['read']['bw'])
                result.append(data['jobs'][int(job)+int(thread)]['read']['lat_ns']['mean']/1000/1000)
                result.append(data['jobs'][int(job)+int(thread)]['read']['clat_ns']["percentile"]["90.000000"]/1000/1000)
                result.append(data['jobs'][int(job)+int(thread)]['read']['clat_ns']["percentile"]["95.000000"]/1000/1000)
                result.append(data['jobs'][int(job)+int(thread)]['read']['clat_ns']["percentile"]["99.000000"]/1000/1000)
                result.append(data['jobs'][int(job)+int(thread)]['read']['clat_ns']["percentile"]["99.900000"]/1000/1000)

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
                result.append(rw_type)
                result.append(data['jobs'][int(job)+int(thread)]['write']['iops'])
                result.append(data['jobs'][int(job)+int(thread)]['write']['bw'])
                result.append(data['jobs'][int(job)+int(thread)]['write']['lat_ns']['mean']/1000/1000)
                result.append(data['jobs'][int(job)+int(thread)]['write']['clat_ns']["percentile"]["90.000000"]/1000/1000)
                result.append(data['jobs'][int(job)+int(thread)]['write']['clat_ns']["percentile"]["95.000000"]/1000/1000)
                result.append(data['jobs'][int(job)+int(thread)]['write']['clat_ns']["percentile"]["99.000000"]/1000/1000)
                result.append(data['jobs'][int(job)+int(thread)]['write']['clat_ns']["percentile"]["99.900000"]/1000/1000)

                
                if 'iodepth' in data['jobs'][int(job)+int(thread)]['job options'].keys():
                    print('get iodepth')
                    print(data['jobs'][int(job)+int(thread)]['job options']['iodepth'])
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
                print('read and write')
            else:
                print("does not match")
            
            result_sum.append(result)
            result = []
        # match rw_type:
        #     case 'read':
        #         print('read')
        #     case 'write':
        #         print('read')
        #     case 'randread':
        #         print('randread')
        #     case 'randwrite':
        #         print('randwrite')
        #     case 'randrw'
        #         print('randrw')
        #     case _:
        #         print("could not found")
    print(result_sum)

    print(tabulate(result_sum, 
        headers=['type', 'iops','bandwidth(MB)','latency_avg(ms)','latency_90%','latency_95%','latency_99%','latency_99.9%','iodepth','blk size', 'device'], 
        tablefmt='orgtbl'))
    
    # rw_type=job_id.split('_')[1]

    # if rw_type.startswith('r'):
    #     rw_type=rw_type[1:]
    # #print 'begin format fio result'
    # ## data[jobs] value is a list,the list only one item for jobnum is 1,if there is more jobs,need to modify
    # if 'w' not in rw_type:
    #     # this is r 
    #     result['type']='read'
    #     result['iops']=data['jobs'][0]['read']['iops']
    #     result['bandwidth']=data['jobs'][0]['read']['bw']

    #     result['latency_avg']=data['jobs'][0]['read']['lat_ns']['mean']/1000/1000
    #     result['latency_900']=data['jobs'][0]['read']['clat_ns']["percentile"]["90.000000"]/1000/1000
    #     result['latency_950']=data['jobs'][0]['read']['clat_ns']["percentile"]["95.000000"]/1000/1000
    #     result['latency_990']=data['jobs'][0]['read']['clat_ns']["percentile"]["99.000000"]/1000/1000
    #     result['latency_999']=data['jobs'][0]['read']['clat_ns']["percentile"]["99.900000"]/1000/1000
    #     print_header(job_id)
    #     #print '{}                |{}                  |{}'.format(result['type'],result['iops'],result['bandwidth'])
    #     print (tabulate([[result['type'], result['iops'],result['bandwidth'],result['latency_avg'], result['latency_900'],result['latency_950'],result['latency_990'],result['latency_999']]], 
    #                      headers=['type', 'iops','bandwidth(MB)','latency_avg(ms)','latency_90%()','latency_95%','latency_99%','latency_99.9%'], tablefmt='orgtbl'))

    # elif 'r' not in rw_type:
    #     # this is w
    #     result['type']='write'
    #     result['iops']=data['jobs'][0]['write']['iops']
    #     result['bandwidth']=data['jobs'][0]['write']['bw']

    #     result['latency_avg']=data['jobs'][0]['write']['lat_ns']['mean']/1000/1000
    #     result['latency_900']=data['jobs'][0]['write']['clat_ns']["percentile"]["90.000000"]/1000/1000
    #     result['latency_950']=data['jobs'][0]['write']['clat_ns']["percentile"]["95.000000"]/1000/1000
    #     result['latency_990']=data['jobs'][0]['write']['clat_ns']["percentile"]["99.000000"]/1000/1000
    #     result['latency_999']=data['jobs'][0]['write']['clat_ns']["percentile"]["99.900000"]/1000/1000
    #     print_header(job_id)
    #     #pprint '{}                |{}                    |{}'.format(result['type'],result['iops'],result['bandwidth'])
    #     print (tabulate([[result['type'], result['iops'],result['bandwidth'],result['latency_avg'], result['latency_900'],result['latency_950'],result['latency_990'],result['latency_999']]], headers=['type', 'iops','bandwidth(MB)','latency_avg(ms)','latency_90%','latency_95%','latency_99%','latency_99.9%'], tablefmt='orgtbl'))

    # else:
    #     result['type']='read and write'
    #     result['read_iops']=data['jobs'][0]['read']['iops']
    #     result['read_bandwidth']=data['jobs'][0]['read']['bw']
    #     result['read_latency_avg']=data['jobs'][0]['read']['lat_ns']['mean']/1000/1000
    #     result['read_latency_900']=data['jobs'][0]['read']['clat_ns']["percentile"]["90.000000"]/1000/1000
    #     result['read_latency_950']=data['jobs'][0]['read']['clat_ns']["percentile"]["95.000000"]/1000/1000
    #     result['read_latency_990']=data['jobs'][0]['read']['clat_ns']["percentile"]["99.000000"]/1000/1000
    #     result['read_latency_999']=data['jobs'][0]['read']['clat_ns']["percentile"]["99.900000"]/1000/1000
        
    #     result['write_iops']=data['jobs'][0]['write']['iops']
    #     result['write_bandwidth']=data['jobs'][0]['write']['bw']
        
    #     result['write_latency_avg']=data['jobs'][0]['write']['lat_ns']['mean']/1000/1000
    #     result['write_latency_900']=data['jobs'][0]['write']['clat_ns']["percentile"]["90.000000"]/1000/1000
    #     result['write_latency_950']=data['jobs'][0]['write']['clat_ns']["percentile"]["95.000000"]/1000/1000
    #     result['write_latency_990']=data['jobs'][0]['write']['clat_ns']["percentile"]["99.000000"]/1000/1000
    #     result['write_latency_999']=data['jobs'][0]['write']['clat_ns']["percentile"]["99.900000"]/1000/1000
    #     print_header(job_id)
    #     #print 'read        |{}             |{}'.format(result['read_iops'],result['read_bandwidth'])
    #     #print 'write       |{}             |{}'.format(result['write_iops'],result['write_bandwidth'])

    #     print (tabulate([['read', result['read_iops'],result['read_bandwidth'],result['read_latency_avg'],result['read_latency_900'],result['read_latency_950'],result['read_latency_990'],result['read_latency_999']],['write',result['write_iops'],result['write_bandwidth'],result['write_latency_avg'],result['write_latency_900'],result['write_latency_950'],result['write_latency_990'],result['write_latency_999']]],headers=['type', 'iops','bandwidth(MB)','latency_avg(ms)','latency_90%','latency_95%','latency_99%','latency_99.9%'], tablefmt='orgtbl'))
    
    #print result
def do_all_fio_jobs(fio_filename,fio_size,fio_runtime):
     try:
         files= os.listdir(PATH)
         for each_file in files:
             do_fio_job(each_file,fio_filename,fio_size,fio_runtime)


     except Exception as e:
         print ('counter exception: {}'.format(str(e)))


def main():
    parser = argparse.ArgumentParser(
        description='xnvme fio bench')
    parser.add_argument('-r','--type', action="store_true",default='nvme',help='info')
    parser.add_argument('-l','--listjobs', action="store_true",help='destination of rsync, cannot be empty')
    parser.add_argument('-p','--printjobs', action="store_true",help='print job')

    parser.add_argument('-j','--job_id',help='job id')
    parser.add_argument('-t','--runtime_of_each_job',help='run_time_of_each_job')
    parser.add_argument('-d','--destination',
                        help='filename parameter in fio, for iscsi it is a device like /dev/sdx, for nas it is directory')
    parser.add_argument('-s','--size',help='size parameter in fio,like 10M or 10G or 1T')


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
        print("运行指定测试用例")
        do_fio_job(options.job_id)

    # def do_fio_job(job_id,filename=None,fio_size=None,fio_runtime=None):
    if options.job_id and options.destination:
        print("指定测试用例，并且指定NVME Disk")
        do_fio_job(options.job_id, filename=options.destination)
        
    if options.runtime_of_each_job and options.runtime_of_each_job:
        print("指定测试用例，并且指定执行时间")
        do_fio_job(options.job_id, fio_runtime=options.runtime_of_each_job)

    if  options.destination and options.size and options.runtime_of_each_job:
       
        if not options.job_id:
            do_all_fio_jobs(options.destination,options.size,options.runtime_of_each_job)



if __name__ == '__main__':

    if os.geteuid() != 0:
        print ("Access the nvme disk must be run as root. Aborting.")
        sys.exit(1)
    else:
        main()
        print("####Finish####")
        sys.exit(0)
