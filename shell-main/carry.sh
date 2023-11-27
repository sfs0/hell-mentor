#!/bin/bash

# 执行 Python 脚本
python3 python/start.py

# 执行其他脚本
# ./backup.sh    # 备份脚本
# ./backup2.sh   # 备份脚本2
./delbr.sh     # 删除某物脚本
./delbr2.sh
# ./imgli.sh     # 图片处理脚本
# ./jssty.sh     # JavaScript 格式化脚本
./readir.sh    # 读取目录脚本
./readir2.sh   # 读取目录脚本2
./reafie.sh    # 读取文件脚本
./reafie2.sh   # 读取文件脚本2
./cnt.sh       # 计数脚本
./backup.sh    # 备份脚本
./backup2.sh   # 备份脚本2

# 复制文件
cp -r news /var/www/html/dist       # 复制 news 文件
cp -r university /var/www/html/dist # 复制 university 文件

