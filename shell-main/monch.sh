#!/bin/bash

# 监控的目录
MONITOR_DIR="/var/www/html/project"

# 日志文件
LOG_FILE="/var/www/html/project/file.log"

# 获取监控目录的绝对路径
MONITOR_DIR_ABSOLUTE=$(realpath "$MONITOR_DIR")

# 如果日志文件不存在，就创建
touch "$LOG_FILE"

# 运行无限循环
while true
do
    # 使用inotifywait命令监控文件系统变动
    inotifywait -r -e create,modify,delete "$MONITOR_DIR" > tmp_log.txt

    # 读取inotifywait输出，记录到日志文件
    while read -r events path
    do
        # 获取事件时间和路径
        timestamp=$(date '+%Y-%m-%d %H:%M:%S')

        # 获取相对路径
        relative_path=$(realpath --relative-to="$MONITOR_DIR_ABSOLUTE" "$path")

        # 获取文件名
        filename=$(basename "$relative_path")

        # 获取变动情况
        change_type="UNKNOWN"
        if grep -q "$timestamp | $relative_path | CREATED" "$LOG_FILE"; then
            change_type="CREATED"
        elif grep -q "$timestamp | $relative_path | MODIFIED" "$LOG_FILE"; then
            change_type="MODIFIED"
        elif grep -q "$timestamp | $relative_path | DELETED" "$LOG_FILE"; then
            change_type="DELETED"
        fi

        # 记录到日志文件
        echo "$timestamp | $filename | $relative_path" >> "$LOG_FILE"
    done < tmp_log.txt

    # 删除临时日志文件
    rm tmp_log.txt

    # 休眠一段时间，可以根据需要调整
    sleep 2
done

