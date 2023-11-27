#!/bin/bash

json_directory="university"  # 指定包含 JSON 数据的目录
output_file="error_summary.txt"   # 构建输出文件名

# 清空或创建输出文件
> "$output_file"

# 用于记录所有错误的数组
all_errors=()

# 使用 find 命令找到指定目录下的所有 JSON 文件
find "$json_directory" -type f -name "*.json" | while read -r json_file; do
    echo "Processing file: $json_file"

    # 用于记录当前文件的错误的数组
    errors=()

    # 检查JSON文件中每个对象的键和值
    while IFS= read -r obj; do
        # 检查是否包含必要的键
        if jq -e 'has("id") and has("Name") and has("Research_direction") and has("img")' <<< "$obj" > /dev/null; then
            # 检查值是否为 "None" 或 ''
            if [ "$(jq -r '.id' <<< "$obj")" == "None" ] || [ "$(jq -r '.id' <<< "$obj")" == "" ] || \
               [ "$(jq -r '.Name' <<< "$obj")" == "None" ] || [ "$(jq -r '.Name' <<< "$obj")" == "" ] || \
               [ "$(jq -r '.Research_direction' <<< "$obj")" == "None" ] || [ "$(jq -r '.Research_direction' <<< "$obj")" == "" ] || \
               [ "$(jq -r '.img' <<< "$obj")" == "None" ] || [ "$(jq -r '.img' <<< "$obj")" == "" ]; then
                errors+=("Error: Value 'None' or empty for some key(s) in an object with id: $(jq -r .id <<< "$obj")")
            else
                echo "Object with id: $(jq -r .id <<< "$obj") is correct."
            fi
        else
            errors+=("Error: Missing required key in an object.")
        fi
    done < <(jq -c '.[]' "$json_file")

    # 将当前文件的错误添加到总错误数组
    all_errors+=("${errors[@]}")
done

# 输出所有错误到文件
if [ ${#all_errors[@]} -eq 0 ]; then
    echo "所有 JSON 文件中每个对象的键和值都是正确的。"
else
    for error in "${all_errors[@]}"; do
        echo "$error" >> "$output_file"
    done
    echo "所有 JSON 文件中的错误信息已保存到 $output_file"
fi

