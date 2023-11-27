#!/bin/bash

directory_path="news"  # 指定 JSON 文件所在的目录

# 使用 find 命令列出指定目录下的所有 JSON 文件
find "$directory_path" -type f -name "*.json" | while read -r json_file; do
    echo "Processing file: $json_file"
    
    # 使用 jq 修改 Research_direction、Contact_information 和 Final_Degree 键下的值并直接写回源文件
    jq '.Research_direction |= gsub("<br/>"; "") | .Contact_information |= gsub("<br/>"; "") | ."Final_Degree" |= gsub("<br/>"; "")' "$json_file" | sponge "$json_file"

    echo  # 添加空行进行分隔
done

