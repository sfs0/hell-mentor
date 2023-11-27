import string
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def teachers_3(url="https://cos.njfu.edu.cn/cxy/main.htm", output_file="output.html"):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # 将网页源码写入文件
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(soup.prettify())


# 调用函数
teachers_3()
