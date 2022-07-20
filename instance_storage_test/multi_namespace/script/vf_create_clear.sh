ROOT_DIR=`pwd`
OWNER=`whoami`

echo $OWNER
if [ $OWNER != "root" ]; then
        echo "WARN: root priviledges required"
        exit
fi

if [ $# != 1 ] ; then
    echo "USAGE: $0 <0-8>"
    echo " e.g.: $0 0   clear VFs of both PF"
    echo " e.g.: $0 4   for each PF create 4 vfs"
    exit
fi

if [[ -z $1 ]]; then
    echo "please input a vf number 0-8"
    echo "9 means clear vfs,  1-8 means for each PF create 1-8 vfs"
    exit
fi


#para chech
if [ $1 -gt 8 ]; then
    echo "the max vf number is 8"
    exit
fi

FUN_CONT=$(lspci -d 10ee: | wc -l)

echo $FUN_CONT

for ((i = 1; i<=2; i++))
do
    BDF=$(lspci -m | grep Xilinx | awk 'NR=='$i' {print $1}')
    # echo $BDF
    SYS_PATH=$(find /sys/bus/pci* -name "*$BDF*" | awk 'NR==1')
    echo $SYS_PATH/sriov_numvfs
    # CMD="echo $1 > $SYS_PATH/sriov_numvfs"
    # echo $CMD
    $(echo $1 > $SYS_PATH/sriov_numvfs)
    if [ $? == 0 ]; then
        if [ $1 -eq 0 ]; then
            echo "Clear VFs success for PF $BDF"
        else
            echo "Create vfs Success for PF $BDF"
        fi
    else
        echo "VF process fail"
    fi
done

# for d in /sys/bus/pci/devices/*; do
#     n=${d#*/iommu_groups/*}; n=${n%%/*}
#     printf 'IOMMU Group %s ' "$n"
#     lspci -nns "${d##*/}"
# done;




#echo 1 > /sys/bus/pci/devices/0000:82:00.0/remove
#echo 1 > /sys/bus/pci/devices/0000:82:00.1/remove

