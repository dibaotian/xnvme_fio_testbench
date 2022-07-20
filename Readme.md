### Readme

#### the test bench is based on the FIO （3.x）

#### https://fio.readthedocs.io/en/latest/fio_doc.html

#### To get the validate nvme driver performance data, please refer https://www.snia.org/forums/cmsi/programs/twg

### Install

#### git clone https://github.com/dibaotian/xnvme_fio_testbench.git

#### cd xnvme_fio_testbench

#### sudo apt install python3-pip

#### pip3 install -r requirements.txt

#### pip3 install tabulate

#### pip3 install psutil

#### pip3 install py-cpuinfo

#### pip3 install pandas

#### pip3 install openpyxl

### Function

#### 1 支持单个fio case 运行

#### 2 支持fio case 分组运行

##### 3 支持指定NVME磁盘运行

#### 4 支持设定运行时长

#### 5 支持自由设置测试磁盘大小

#### 6 支持 iops(k) |   bandwidth(MB) |   latency_avg(ms) |   latency_90% |   latency_95% |   latency_99% |   latency_99.9%  数据统计

#### 7 支持按照设定频率采集运行时刻iops  bandwidth  latency的数据，并进行图表绘制和统计

#### 8 支持统计文件生成xlxs文件

### Restriction

#### 1 Python3 运行

#### 2 适配FIO 3.x， FIO2.x 没有进过测试

#### 3 适配libaio engine， 其它ioengine 没有测试

#### 4 nvme disk 访问需要root权限

### usage

usage: xnvme_fio_bench.py [-h] [-r] [-l] [-p] [-j JOB_ID] [-g GROUP_ID]
                          [-t RUNTIME_OF_EACH_JOB] [-d DESTINATION] [-s SIZE]

optional arguments:
  -h, --help            show this help message and exit
  -r, --type            info
  -l, --listjobs        destination of jobs, cannot be empty
  -p, --printjobs       print job
  -j JOB_ID, --job_id JOB_ID
                        job id
  -g GROUP_ID, --group_id GROUP_ID
                        group id， cannot be empty
  -t RUNTIME_OF_EACH_JOB, --runtime_of_each_job RUNTIME_OF_EACH_JOB
                        run time of each job
  -d DESTINATION, --destination DESTINATION
                        filename parameter in fio, for NVME it is a device
                        like /dev/nvme0n1
  -s SIZE, --size SIZE  size parameter in fio,like 100M or 10G or 1T

usage: plot_fio_bw_iops_log.py [-h] [-f FILE] [-l LABLE] [-t TYPE]

xnvme fio bench plot tool

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  bw/iops/latency file
  -l LABLE, --lable LABLE
                        lable
  -t TYPE, --type TYPE  file log type bw/io/la

运行时将xnvme_fio_bench.py，plot_fio_bw_iops_log.py以及fio配置文件放在同一个目录下

运行./xnvme_fio_bench.py -j  fio_seq_read -t 10

例如：

root@Z690:/home/xilinx/Documents/minx/xnvme_fio_testbench_upstream/example# ./xnvme_fio_bench.py -j fio_seq_read -t 10
CPU:  12th Gen Intel(R) Core(TM) i7-12700K X86_64 64bit 20core 1670131000Hz
内存: 31.13799285888672G
系统： Linux Z690 5.4.0-122-generic #138~18.04.1-Ubuntu SMP Fri Jun 24 14:14:03 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux
工具： fio-3.1
开始执行用例fio_seq_read，设置运行10秒

2022年 07月 20日 星期三 17:12:03 CST
Start to process fio_seq_read
========= fio spend 0.17587899764378864 mins=======
========= run time: Wed Jul 20 17:12:14 2022=======
=========  result of fio_seq_read  =========
| type      |   iops(k) |   bandwidth(MB) |   latency_avg(us) |   latency_90% |   latency_95% |   latency_99% |   latency_99.9% |   iodepth | blk size   | device        |
|-----------+-----------+-----------------+-------------------+---------------+---------------+---------------+-----------------+-----------+------------+---------------|
| read_0_0  |   44.6013 |         174.224 |           179.023 |       284.672 |       333.824 |       452.608 |         602.112 |         8 | 4k         | /dev/nvme0n1  |
| read_1_0  |   43.5875 |         170.264 |           183.176 |       288.768 |       346.112 |       468.992 |         618.496 |         8 | 4k         | /dev/nvme1n1  |
| read_2_0  |   44.7506 |         174.807 |           178.416 |       280.576 |       329.728 |       448.512 |         593.92  |         8 | 4k         | /dev/nvme2n1  |
| read_3_0  |   44.7366 |         174.752 |           178.448 |       280.576 |       333.824 |       452.608 |         602.112 |         8 | 4k         | /dev/nvme3n1  |
| read_4_0  |   44.4205 |         173.517 |           179.741 |       280.576 |       329.728 |       452.608 |         593.92  |         8 | 4k         | /dev/nvme4n1  |
| read_5_0  |   44.435  |         173.573 |           179.672 |       280.576 |       333.824 |       452.608 |         593.92  |         8 | 4k         | /dev/nvme5n1  |
| read_6_0  |   44.5282 |         173.938 |           179.314 |       276.48  |       329.728 |       444.416 |         585.728 |         8 | 4k         | /dev/nvme6n1  |
| read_7_0  |   44.681  |         174.535 |           178.68  |       280.576 |       329.728 |       452.608 |         593.92  |         8 | 4k         | /dev/nvme7n1  |
| read_8_0  |   44.5009 |         173.831 |           179.415 |       284.672 |       333.824 |       448.512 |         593.92  |         8 | 4k         | /dev/nvme8n1  |
| read_9_0  |   44.4577 |         173.662 |           179.569 |       280.576 |       329.728 |       448.512 |         593.92  |         8 | 4k         | /dev/nvme9n1  |
| read_10_0 |   44.0236 |         171.967 |           181.356 |       288.768 |       342.016 |       464.896 |         618.496 |         8 | 4k         | /dev/nvme10n1 |
| read_11_0 |   44.0287 |         171.986 |           181.362 |       288.768 |       342.016 |       460.8   |         602.112 |         8 | 4k         | /dev/nvme11n1 |
| read_12_0 |   43.849  |         171.285 |           182.094 |       288.768 |       342.016 |       464.896 |         610.304 |         8 | 4k         | /dev/nvme12n1 |
| read_13_0 |   43.9812 |         171.801 |           181.532 |       288.768 |       342.016 |       464.896 |         602.112 |         8 | 4k         | /dev/nvme13n1 |
| read_14_0 |   43.6048 |         170.331 |           183.091 |       288.768 |       346.112 |       468.992 |         618.496 |         8 | 4k         | /dev/nvme14n1 |
| read_15_0 |   43.7559 |         170.921 |           182.454 |       288.768 |       346.112 |       468.992 |         610.304 |         8 | 4k         | /dev/nvme15n1 |
| read_16_0 |   43.9041 |         171.5   |           181.848 |       288.768 |       342.016 |       464.896 |         610.304 |         8 | 4k         | /dev/nvme16n1 |
| read_17_0 |   43.8321 |         171.219 |           182.15  |       288.768 |       342.016 |       464.896 |         618.496 |         8 | 4k         | /dev/nvme17n1 |

运行结束，回生成data 和log两个文件夹

data下记录了fio的输出统计结果， log文件夹下记录了bw， iops， latency 的中间采集数据，可以利用plot_fio_bw_iops_log.py 对数据进行绘图

支持FIO case 分组运行

在目录下创建group文件夹，将要分组运行的fio配置文件软连接到文件加内

执行 ./xnvme_fio_bench.py -g  group 即可

### bug

##### bug1：多个[job]情况下，[global] 配置group reporting会报错误

### FIO 配置参数

##### fio支持的读写模式包括顺序读，随机读，顺序写，随机写，混合随机读写，混合顺序读写。

##### 常用参数包括引擎，队列深度，线程，block，是否裸设备，读写方式，大小/耗时，跳过缓存等

##### parameter

##### filename=/dev/nvme0n1    支持文件系统或者裸设备,压测多个磁盘 --filename=/dev/nvme0n1:/dev/nvme1n1

##### direct=1                 测试过程绕过机器自带的buffer（绕过操作系统的cache），使测试结果更真实

##### rw=randwread             测试随机读的I/O

##### rw=randwrite             测试随机写的I/O

##### rw=randrw                测试随机混合写和读的I/O

##### rw=read                  测试顺序读的I/O

##### rw=write                 测试顺序写的I/O

##### rw=rw                    测试顺序混合写和读的I/O

##### bs=4k                    单次io的块文件大小为4k,一般来说块大小为 512B  4K 16K .....1M、4M 这样的扇区大小（512字节）的倍数，小于16K的文件，一般算作小文件，大于16K的文件属于大文件

##### bsrange=512-2048         同上，指定定数据块的大小范围

##### size=50g                 寻址空间，这里是以每次4k的io进行50G的空间测试, size=100%?

##### numjobs=30               本次的测试线程为30

##### runtime=1000             测试时间为1000秒，如果不写则一直将5g文件分4k每次写完为止

##### ioengine=libaio          负载引擎，发起异步IO读写请求，io引擎使用libaio引擎， 也可以指定其它方式，例如pync.libaio:Linux native asynchronous I/O. Note that Linux may only support queued behavior with non-buffered I/O (set direct=1 or buffered=0). This engine defines engine specific options.

##### iodepth                  队列深度，一次提交I/O请求的数目，（只对异步I/O引擎有用），队列深度影响IOPS

##### rwmixwrite=30            在混合读写的模式下，写占30%

##### group_reporting          关于显示结果的，汇总每个进程的信息

##### lockmem=1g               只使用1g内存进行测试

##### zero_buffers             用0初始化系统buffer

##### nrfiles=8                每个进程生成文件的数量

##### stonewall                确保当前执行块和下个执行块串行执行

##### randrepeat=1             对于随机IO负载，配置生成器的种子，使得路径是可以预估的，使得每次重复执行生成的序列是一样的。randrepeat：默认是True, 如果不设置randrepeat=0这个参数不会影响seqread，但会影响seqwrite,randwrite,randread.

##### loops=int                重复运行某个job多次，默认是1

##### ramp_time = 30	       定义测试的热身时间，以秒为单位。热身时间不计入测试统计。

### FIO输出结果

##### io=执行了多少M的IO

##### bw=平均IO带宽

##### iops=IOPS

##### runt=线程运行时间

##### slat=提交延迟

##### clat=完成延迟

##### lat=响应时间

##### bw=带宽

##### cpu=利用率

##### IO depths=io队列

##### IO submit=单个IO提交要提交的IO数

##### IO complete=Like the above submit number, but for completions instead.

##### IO issued=The number of read/write requests issued, and how many of them were short.

##### IO latencies=IO完延迟的分布

##### io=总共执行了多少size的IO

##### aggrb=group总带宽

##### minb=最小.平均带宽.

##### maxb=最大平均带宽.

##### mint=group中线程的最短运行时间.

##### maxt=group中线程的最长运行时间.

##### ios=所有group总共执行的IO数.

##### merge=总共发生的IO合并数.

##### ticks=Number of ticks we kept the disk busy.

##### util=磁盘利用率

##### 可以使用iostat进行结果交叉验证

###### iostat -mx 1 -d `<device>`

###### iostat -c -d -x -t -m /dev/nvme0n1 1

###### rrqm/s: 每秒对该设备的读请求被合并次数，文件系统会对读取同块(block)的请求进行合并

###### wrqm/s: 每秒对该设备的写请求被合并次数

###### r/s: 每秒完成的读次数

###### w/s: 每秒完成的写次数

###### rkB/s: 每秒读数据量(kB为单位)

###### wkB/s: 每秒写数据量(kB为单位)

###### avgrq-sz:平均每次IO操作的数据量(扇区数为单位)

###### avgqu-sz: 平均等待处理的IO请求队列长度，队列长度越短越好

###### await: 平均每次IO请求等待时间(包括等待时间和处理时间，毫秒为单位)

###### svctm: 平均每次IO请求的处理时间(毫秒为单位)

###### %util: 采用周期内用于IO操作的时间比率，在统计时间内所有处理IO时间，除以总共统计时间。例如，如果统计间隔1秒，该设备有0.8秒在处理IO，而0.2秒闲置，那么该设备的%util = 0.8/1 = 80%，所以该参数表示了设备的繁忙程度

### 注意事项

NAND-based SSS device controllers map Logical Addresses (LBA) to Physical Blocks Addresses (LBA) on the NAND media, in order to achieve the best NAND performance and endurance. The SSS device manages this LBA-to-PBA mapping with internal processes that operate independently of the host.

The sum of this activity is referred to as “flash management”.

The performance of the flash management during a test, and hence the overall performance of the SSS device during the test, depends critically on:

1) Write History and Preconditioning: The state of the device prior to the test
2) Workload Pattern: Pattern of the I/O (r/w mix, block size, etc.) written to device during test
3) Data Pattern: The actual bits in the data payload written to the device

The methodologies defined in the SSS Performance Test Specification (SSS PTS) attempt to create consistent conditions for items 1-3 so that the only variable is the device under test.

### precondition

##### why precondition

##### To truly profile an SSD you have to use the entire drive. If you restrict the size written to a fraction of the drive an SSD will use the remainder as increased overprovision to reduce write amplification and performance. Also, most SSD's will not access NAND for reads to LBAs not already written. When you measure a read to an unwritten LBA you actual measure the speed at which the SSD can create 0's and ship them back.

##### Bsasic steps to follow to get reliable data at the end:

##### 1. Secure Erase SSD

##### why？The erase applies to all user data, regardless of location (e.g., within an exposed LBA, within a cache, within deallocated LBAs, etc). Defaults to 0. There are two types of secure erase. The User Data Erase erases all user content present in the NVM subsystem. The Cryptographic Erase erases all user content present in the NVM subsystem by deleting the encryption key with which the user data was previously encrypted.

##### 2. Fill SSD with sequential data twice of it's capacity. This will gurantee all available memory is filled with a data including factory provisioned area. DD is the easiest way for this: dd if=/dev/zero bs=1024k of=/dev/"devicename"

#### 3. If you're running sequential workload to estimate the read or write throughput then skip the next step.

#### 4. Fill the drive with 4k random data. The same rule, total amount of data is twice drive's capacity.

##### 5. Run your workload. Usually meassurements starts after 5 minutes of runtime in order to let the SSD FW adopting to the workload. It's called sustained performance state. This time depends on the SSD Vendor/SKU/capacity.

### How to test the nvme

### Test mechanics

##### Preconditioning

##### Common measurement tools used to construct a write-saturation plot

##### How system configurations can affect measured performance

##### Repeatability: Given the same set of inputs, the results should always be within the expected run-to-run variance.

##### SSD performance can change as the drive is being written, our Enterprise performance measurement focuses on the steady state performance region.

##### 1. Purge: Regardless of what has been done previously to the nvme, a purge puts the drive in a known, fixed state that emulates the state in which the drive would be received from the manufacturer, the fresh-out-of-box (FOB) state.

##### uses the secure erase or sanitize commands with NVME disk

##### place the sample SSD in an FOB state

##### secure erase or sanitize is not the same as format (format may or may not restore the SSD to the FOB state)

##### 2. Precondition: for workload-independent precondition, write the drive with 128KB sequential transfers aligned to 4K boundaries over 2X the drive’s advertised capacity.

### how to accurately measure nvme disk performance consistently and repeatabily?

##### refer https://www.snia.org/forums/cmsi/programs/twg

#### goal

##### nvme disk performance measurement (accuracy, consistency, and repeatability)

#### problem

#### each time test got different performance data

#### Reason

##### nvme disk performance is sensitive to their write-history and how full their capacity is and system variations

##### write-history sensitivity

##### full

##### system variations

##### How

##### purge + preconditioning before each performance running

##### Put nvme disk in the same state at the beginning of each test, precondition it the same way for each test and stimulate it to steady state performance

##### Purge to Return the nvme disk to the FOB state for each test is key to precise,consistent performance measurement.
