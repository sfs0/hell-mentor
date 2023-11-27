import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def teachers_3(url="https://waiyuan.njfu.edu.cn//szdw/szml/index.html"):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # 找到符合条件的 <td> 标签
    td_tag = soup.find("td", {"colspan": "2", "valign": "top"})

    # 找到 <a> 标签并提取 href 属性
    links = [a.get("href") for a in td_tag.find_all("a", href=True)]

    return list(set(links))  # 去重并返回


# 调用函数
links_list = teachers_3()
print(len(links_list))
print("提取到的链接列表:", links_list)
