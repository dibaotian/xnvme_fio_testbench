if [ $# != 1 ] ; then
    echo "USAGE: $0 <1-10>"
    echo " e.g.: $0 4 create 4 namespace in each controller "
    exit
fi

ls /dev/nvme0
if [ $? == 0 ]; then
    echo "nvme0 controller is ready"
else
    echo "Error:nvme0 controller is not ready"
    exit
fi

ls /dev/nvme1
if [ $? == 0 ]; then
    echo "nvme1 controller is ready"
else
    echo "Error:nvme1 controller is not ready"
    exit
fi

if [ $1 -gt 10 ]; then
    echo "$0 <1-10>"
    exit
fi

# nv_size0=(150029536 28130538 9376846 93768460 8784423 46884230 56261076 65637922 75014768 84391614 97864460 50980230) 
# nv_size1=(46925190 27538115 75096688 14065269 18757788 23442115 28171498 32818961 37589304 42195807 46291807 18161269) 
nv_size0=(31250000  31250000  31250000  31250000  31250000  31250000  31250000  31250000  31250000  31250000  31250000  31250000) 
nv_size1=(31250000  31250000  31250000  31250000  31250000  31250000  31250000  31250000  31250000  31250000  31250000  31250000) 
for ((j = 0; j<2; j++))
do
    for ((i = 1; i<=$1; i++))
    do
        # nvme create-ns /dev/nvme0 --nsze=4102369 --ncap=4102369 --block-size=4096 --dps=0
        # nvme create-ns /dev/nvme0 -s 195312500 -c 195312500 -f 0 -d 0 -m 0
        # RET_CRT=$(nvme create-ns /dev/nvme$j -s 195312500 -c 195312500 --block-size=4096 -d 0 -m 0)
        if [ $j -eq 0 ]; then
            RET_CRT=$(nvme create-ns /dev/nvme0 -s ${nv_size0[i]} -c ${nv_size0[i]} -f 2 -d 0 -m 0)
        fi

        if [ $j -eq 1 ]; then
            RET_CRT=$(nvme create-ns /dev/nvme1 -s ${nv_size1[i]} -c ${nv_size1[i]} -f 2 -d 0 -m 0)
        fi
                  
        echo $RET_CRT

        if [ $? == 0 ]; then
            echo ""
        else
            echo "Error:create-ns /dev/nvme$j fail"
        fi

        NS=${RET_CRT#*nsid:}

        RET_ATT=$(nvme attach-ns /dev/nvme$j -c 0 -n $NS)
        echo $RET_ATT
        if [ $? == 0 ]; then
            echo " "
        else
            echo "Error:attach-ns /dev/nvme$j fail"
        fi

    done
done

nvme reset /dev/nvme0
if [ $? == 0 ]; then
    echo "Reset nvme0 success"
else
    echo "Error: Reset nvme0 fail"
fi

nvme reset /dev/nvme1
if [ $? == 0 ]; then
    echo "Reset nvme1 success"
else
    echo "Error: Reset nvme1 fail"
fi