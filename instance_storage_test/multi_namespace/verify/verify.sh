echo $1
# fio --filename=/dev/nvme0n1 --ioengine=libaio --name=write_test --direct=1 --thread=1 --iodepth=16 --rw=write --bs=4k --numjobs=8 --size=100G --norandommap --fallocate=none --verify=md5 --do_verify=1 --verify_dump=1 --output=verify.log
fio --filename=$1 --ioengine=libaio --name=write_test --direct=1 --iodepth=16 --rw=randwrite --bs=128k --numjobs=8 --size=100G --norandommap --fallocate=none --verify=md5 --do_verify=1 --verify_dump=1 --output=verify.log