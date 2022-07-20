#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: minx@amd.com
# based on the Python3
# it is a dangeous execute 

import os
import re
import sys
import time
import subprocess
import argparse

# nvme id-ctrl /dev/nvme0 -H | grep "Format \|Crypto Erase\|Sanitize"
# to format /dev/nvme0 with a crypto erase to namespace 1:
# nvme format /dev/nvme0 -s 2 -n 1
# subprocess.getoutput("nvme id-ctrl /dev/nvme0 -H | grep 'Format \|Crypto Erase\|Sanitize'")

# hexdump /dev/nvme0n1 -n 100

# device = "/dev/nvme0n1"
# subprocess.getoutput("date")
# print("start to dd {}, it will take over 40 mins for 3.84T nvme disk , please wait".format(device))
# start = time.time()
# subprocess.getoutput("dd if=/dev/zero bs=1024k of=/{}".format(device))
# end = time.time()
# print("========= dd spend {} mins=======".format(float(end-start)/float(60.00)))

    
# nvme id-ctrl /dev/nvme0 -H | grep "Format \|Crypto Erase\|Sanitize"
# to format /dev/nvmex with a crypto erase to namespace 1:
# nvme format /dev/nvme0 -s 1 -n 1
# subprocess.getoutput("nvme id-ctrl /dev/nvme0 -H | grep 'Format \|Crypto Erase\|Sanitize'")

# hexdump /dev/nvme0n1 -n 100

def do_fio_job(job_id,filename):

    # todo 打印开始时间
    try:
        with open(job_id,'r') as f:
            lines=f.readlines()
        #print 'befor patch ,the conf is {}'.format(lines)
        for index,item in enumerate(lines):
            if 'filename=' in item:
                lines[index]='filename={}\n'.format(filename)

        with open(filename,'w') as f:
            f.writelines(lines)

        #print "patch fio conf ok: {}".format(file)
        output=subprocess.getoutput("date")
        print('start preconditioning at {}'.format(output))
        start = time.time()

        # fio job_id

        output=subprocess.getoutput("fio {} --output-format=json".format(filename))
        # p = subprocess.Popen("fio {}".format(job_id), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # try:
        #     buff = p.communicate()
        #     stritem = buff[0]
        #     str_list = re.split(r'  +|\n', stritem)
        #     print(str_list)
        # except Exception as e:
        #     print ("error {}".format(e))
        #     sys.exit(1)
        #     p.stdout.close()

        end = time.time()
        print("========= preconditioning spend {} mins=======".format(float(end-start)/float(60.00)))
    except Exception as e:
        # print(output)
        print ('do_fio_job exception: {}'.format(str(e)))

def main():

    parser = argparse.ArgumentParser(description='purge and preconditioning for nvme performance test')
    parser.add_argument('-d','--devices', action='append', help='device file')
    # parser.add_argument('-j','--job', help='fio precondition file')

    options = parser.parse_args()

    # if options.devices and options.job:
    if options.devices:
        devices = options.devices
        # job = options.job
        print(devices)
    else:
        print("please input a nvme device")
        exit(-1)

    # format /dev/nvme<x>n<y> with a crypto erase:
    # output=subprocess.getoutput("fio {} --output-format=json".format(run_conf))

    for device in devices:
        print("start to format device {}, it may take sereval mins, please wait".format(device))
        output = subprocess.getoutput("nvme format {} -s 1".format(device))
        if output.split(" ")[0] == 'Success':
            print("FOB {} success".format(device))
        else:
            print("FOB {} fail, please check if device exist".format(device))
            exit(1)
        
        # do_fio_job("preconditioning.fio",device)
        # do_fio_job(job,device)

if __name__ == '__main__':

    if os.geteuid() != 0:
        print ("Access the nvme disk must be run as root. Aborting.")
        sys.exit(1)
    else:
        main()
        sys.exit(0)