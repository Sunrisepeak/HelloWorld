# pre-install:
#     sudo apt-get install build-essential linux-headers-$(uname -r)

arg=$1
# add "" to avoid null; -> line 6: [: ==: unary operator expected
if [ "$arg" == "module" ]; then
    make -C /lib/modules/$(uname -r)/build M=`pwd` modules
elif [ "$arg" == "clean" ]; then
    make -C /lib/modules/$(uname -r)/build M=$(pwd) clean
    #make -C /lib/modules/$(uname -r)/build M=$(pwd) mrproper
else
    echo cmd: module/clean
    echo shell cmd:
    echo -     sudo insmod your.ko
    echo -     lsmod
    echo -     sudo rmsmod your.ko
    echo -     dmesg
fi
# sudo insmod your.ko
# sudo rmmod your

# dmesg