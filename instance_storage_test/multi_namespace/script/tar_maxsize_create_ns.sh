# 删除所有nvme 
nvme delete-ns /dev/nvme0 -n 0xFFFFFFFF
nvme reset /dev/nvme0

nvme delete-ns /dev/nvme1 -n 0xFFFFFFFF
nvme reset /dev/nvme1

# max size 
# tnvmcap   : 3840755982336
# 3840755982336/4K   937684566
                  
nvme create-ns /dev/nvme0 -s 937684566 -c 937684566 -f 2 -d 0 -m 0
nvme attach-ns /dev/nvme0 -c 0 -n 1
nvme reset /dev/nvme0

# max size
nvme create-ns /dev/nvme1 -s 937684566 -c 937684566 -f 2 -d 0 -m 0
nvme attach-ns /dev/nvme1 -c 0 -n 1
nvme reset /dev/nvme1

nvme list
