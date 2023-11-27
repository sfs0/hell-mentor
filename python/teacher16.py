import string
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def teachers_16(url="https://cee.njfu.edu.cn/szdw/zzjs/"):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    if response.status_code != 200:
        print(f"无法访问页面：{url}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    # 查找符合条件的 TABLE 标签
    tables = soup.find_all(
        "table",
        {
            "cellspacing": "1",
            "cellpadding": "0",
            "width": "100%",
            "align": "center",
            "border": "0",
        },
    )

    # 提取 TABLE 下所有 a 标签的 href
    links = []
    for table in tables:
        links.extend([a.get("href") for a in table.find_all("a", href=True)])

    return links


# 调用函数
found_hrefs = teachers_16()
print(len(found_hrefs))
print("找到的链接列表:", found_hrefs)
