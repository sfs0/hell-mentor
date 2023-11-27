#!/bin/bash

# 源目录
source_dir="/var/www/html/project/python"

# 目标目录，用于存储备份
backup_dir="/var/www/html/project/backup1"

# 在备份目录中创建日期命名的子目录
backup_subdir="$backup_dir/backup_$(date +"%Y%m%d_%H%M%S")"

# rsync 命令，-a 选项表示彻底复制，-v 表示详细输出
rsync -av "$source_dir/" "$backup_subdir/"

# 输出备份完成消息
echo "Backup completed. Files are backed up to: $backup_subdir"

