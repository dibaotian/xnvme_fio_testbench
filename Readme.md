### Readme

### the test bench is based on the FIO
### https://fio.readthedocs.io/en/latest/fio_doc.html

### 功能
##### 支持单个case 运行
##### 支持分组case 运行

### restriction
##### 不支[job]下group reporting设置, group reporting 必须放在[global]下面
##### 运行时候，size 不能小于 block size
##### numjobs 必须设置在[jobsx]下,不能在[global]
##### 多个[jobx] ，每个[job] 指向不同的nvme disk 的时候，[global]不能使用 direct=1

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
##### bs=4k                    单次io的块文件大小为4k
##### bsrange=512-2048         同上，指定定数据块的大小范围
##### size=50g                 寻址空间，这里是以每次4k的io进行50G的空间测试，, size=100%,对整个磁盘测试
##### numjobs=30               本次的测试线程为30
##### runtime=1000             测试时间为1000秒，如果不写则一直将5g文件分4k每次写完为止
##### ioengine=libaio          负载引擎，发起异步IO读写请求，io引擎使用libaio引擎， 也可以指定其它方式，例如pync
#####                          libaio:Linux native asynchronous I/O. Note that Linux may only support queued behavior with non-buffered I/O (set direct=1 or buffered=0). This engine defines engine specific options.
##### iodepth                  队列深度，只有使用libaio的时候有意义，队列深度影响IOPS
##### rwmixwrite=30            在混合读写的模式下，写占30%
##### group_reporting          关于显示结果的，汇总每个进程的信息
##### lockmem=1g               只使用1g内存进行测试
##### zero_buffers             用0初始化系统buffer
##### nrfiles=8                每个进程生成文件的数量
##### stonewall                确保当前执行块和下个执行块串行执行

##### Result
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

##### P5510
##### 1 Random read & write IOPS
#####  block size  4k/8k
##### 2 Sequential read & write IOPS

##### 3 Typical latency 
##### 4 quality of service

