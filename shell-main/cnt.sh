#!/bin/bash

directory_path="news" # 指定目录的路径
output_file="file_count_summary.txt" # 指定输出文件路径

# 清空或创建输出文件
> "$output_file"

# 使用 find 命令列出指定目录下的所有文件和目录
find "$directory_path" -type d | while read -r dir; do
    echo "Directory: $dir" >> "$output_file"

    # 统计每个目录下不同类型文件的数量
    find "$dir" -maxdepth 1 -type f | sed -n 's/.*\.//p' | sort | uniq -c | while read -r count type; do
        echo "  File type: $type, Number of files: $count" >> "$output_file"
    done

    # 输出每个目录的总文件数量
    total_files=$(find "$dir" -maxdepth 1 -type f | wc -l)
    echo "  Total files: $total_files" >> "$output_file"

    echo  >> "$output_file" # 添加空行进行分隔
done

# 输出指定目录中的总文件数
total_files_all=$(find "$directory_path" -type f | wc -l)
echo "Total files in $directory_path: $total_files_all" >> "$output_file"

echo "结果已保存到 $output_file"

