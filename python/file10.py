def read_and_remove_duplicates(
    input_file="output.txt", output_file="output_no_duplicates.txt"
):
    # 用集合来存储唯一链接
    unique_links = set()

    # 读取文件并去重
    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            link = line.strip()
            if link:
                unique_links.add(link)

    # 将唯一链接写入新文件
    with open(output_file, "w", encoding="utf-8") as file:
        for link in unique_links:
            file.write(link + "\n")


# 调用函数
read_and_remove_duplicates()
