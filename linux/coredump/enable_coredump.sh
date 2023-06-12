#!/bin/bash

DUMP_PATH=`pwd`/crashdump

# 检查当前用户是否具有sudo权限
if [ "$(id -u)" != "0" ]; then
  echo "请使用sudo运行此脚本"
  exit 1
fi

# 开启Coredump
echo "开启Coredump..."
echo 2 > /proc/sys/fs/suid_dumpable
echo "$DUMP_PATH/%e.%p.%t.coredump" > /proc/sys/kernel/core_pattern

# 创建Coredump保存目录
echo "创建Coredump保存目录..."
mkdir -p $DUMP_PATH
chmod 777 $DUMP_PATH

echo "Coredump功能已开启 配置信息如下:"
cat /proc/sys/fs/suid_dumpable
cat /proc/sys/kernel/core_pattern