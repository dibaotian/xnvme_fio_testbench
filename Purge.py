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

if os.geteuid() != 0:
    print ("Access the nvme disk must be run as root. Aborting.")
    sys.exit(1)


# nvme id-ctrl /dev/nvme0 -H | grep "Format \|Crypto Erase\|Sanitize"
# to format /dev/nvme0 with a crypto erase to namespace 1:
# nvme format /dev/nvme0 -s 2 -n 1
# subprocess.getoutput("nvme id-ctrl /dev/nvme0 -H | grep 'Format \|Crypto Erase\|Sanitize'")

# Sanitize主要包含两个阶段，向SSD发sanitize命令，后台异步执行擦除操作
# 对应两个时间 completion of the Sanitize command(命令的完成)和completion of the sanitize operation(操作的完成)，命令的完成不代表操作的完成。
# 对于用户而言，sanitize命令是在异步完成用户数据删除前返回完成，看到的执行时间相比format更短，format必须彻底删除数据后才返回完成
# Sanitize status log关键字段：
# Sanitize Progress(SPROG)字段代表sanitize完成进度，是指异步从NAND彻底删除数据的进度，以65536为分母，65535即进度完成100%。
# Sanitize Status(SSTAT)字段记录最近一次完成的sanitize状态，0x101代表[2:0]中第0 bit置“1”，即说明最近一次sanitize执行成功。
# Sanitize Command Dword 10 Information (SCDW10)字段代表完成Sanitize – Command Dword 10的操作类型，0x2即0x010b，完成的是Block Erase sanitize操作。

subprocess.getoutput("nvme sanitize-log")
device = "/dev/nvme0n1"
print("start to dd {}, it will take over 20 mins for 3.84T nvme disk , please wait".format(device))
start = time.time()
subprocess.getoutput("dd if=/dev/zero bs=1024k of=/{}".format(device))
end = time.time()
print("========= dd spend {} mins=======".format(float(end-start)/float(60.00)))


