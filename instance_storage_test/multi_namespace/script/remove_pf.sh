ROOT_DIR=`pwd`
OWNER=`whoami`

# echo $OWNER
if [ $OWNER != "root" ]; then
        echo "WARN: root priviledges required"
        exit
fi

FUN_CONT=$(lspci -d 10ee: | wc -l)

# echo $FUN_CONT

if [ $FUN_CONT -ne 2 ]; then
	echo "Please check the if the virtial function is deleted"
	exit
fi

for ((i = 1; i<=2; i++))
do
    echo $i 
    # echo "get BDF"
    BDF=$(lspci -d 10ee: | cut -d' ' -f 1 | awk NR==1)
    echo $BDF
    if [[ -z $BDF ]]; then
        echo "[ERROR : can not find the nvme device]"
        exit
    fi

    SYS_PATH=$(find /sys/bus/pci* -name "*$BDF*" | awk 'NR==1')
    # # echo $SYS_PATH/remove
    ls $SYS_PATH/remove
    if [ $? == 0 ]; then
        echo 1 > $SYS_PATH/remove
        if [ $? == 0 ]; then
            echo "remove $BDF success"
            sleep 3
        else
            echo "remove $BDF fail"
        fi
    else
        echo "Can not find $BDF system process file"
    fi
done



