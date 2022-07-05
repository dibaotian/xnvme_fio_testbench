### Readme

### the test bench is based on the FIO （3.x）
### https://fio.readthedocs.io/en/latest/fio_doc.html

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
##### 1 支持单个case 运行
##### 2 支持分组case 运行
##### 3 支持指定NVME磁盘运行
##### 4 支持自由设定运行时长
##### 5 支持自由设置测试磁盘大小
##### 6 支持打印配置文件
##### 7 支持 iops(k) |   bandwidth(MB) |   latency_avg(ms) |   latency_90% |   latency_95% |   latency_99% |   latency_99.9%  数据统计
##### 8 支持统计文件生成xlxs文件

### Restriction
##### 1 Python3 运行
##### 2 适配FIO 3.x， FIO2.x 没有进过测试
##### 3 适配libaio engine， 其它ioengine 没有测试

#### bug
##### bug1：多个[job]情况下，[global] 配置group reporting会报错误


### about FIO configure parameter and result
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

### Result
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

##### Concern
##### 1 Random read & write IOPS
##### 2 Sequential read & write bandwidth
##### 3 Typical latency 
##### 4 quality of service

##### iostat
###### iostat -mx 1 -d <device>
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


