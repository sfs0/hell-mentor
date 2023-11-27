#!/bin/bash

json_directory="news"  # 指定包含 JSON 数据的目录

# 使用 find 命令找到指定目录下的所有 JSON 文件
find "$json_directory" -type f -name "*.json" | while read -r json_file; do
    echo "Processing file: $json_file"

    # 使用 jq 修改 Research_direction 键下的值并覆盖源文件
    jq '.Research_direction |= sub(".*研究领域："; "")' "$json_file" > "$json_file.tmp" \
    && mv "$json_file.tmp" "$json_file"
done

