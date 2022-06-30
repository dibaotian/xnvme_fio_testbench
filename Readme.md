### Readme

### 功能
#### 支持单个case 运行
#### 支持分组case 运行

### restriction
##### 不支[job]下group reporting设置, group reporting 必须放在[global]下面
##### 运行时候，size 不能小于 block size
##### numjobs 必须设置在[jobsx]下,不能在[global]
##### 多个[jobx] ，每个[job] 指向不同的nvme disk 的时候，[global]不能使用 direct=1

#### bug
##### bug1：多个[job]情况下，[global] 配置group reporting会报错误