#!/bin/bash

# 指定包含 JSON 数据的目录
json_directory="university"

# 输出文件将包含无法打开的链接
output_file="unreachable_links.txt"

# 清空或创建输出文件
> "$output_file"

# 使用 find 命令找到指定目录下的所有 JSON 文件
find "$json_directory" -type f -name "*.json" | while read -r input_file; do
    echo "Processing file: $input_file"

    # 使用 jq 解析 JSON，提取链接，并检查是否可达
    jq -r '.[].img' "$input_file" | while read -r url; do
        # 使用 curl 检查链接是否可达
        if curl -s --head "$url" | head -n 1 | grep "HTTP/1.[01] [23].." > /dev/null; then
            echo "Link is reachable: $url"
        else
            echo "Link is unreachable: $url"
            # 将无法打开的链接追加到输出文件
            echo "$url" >> "$output_file"
        fi
    done
done

