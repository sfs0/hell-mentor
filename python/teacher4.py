import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def teachers_4(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # 查找符合条件的 TABLE 标签
    table = soup.find(
        "table",
        {
            "cellspacing": "1",
            "cellpadding": "0",
            "width": "96%",
            "align": "center",
            "border": "0",
            "bgcolor": "#CCCCCC",
        },
    )

    # 安全检查，如果没有找到符合条件的 table，则返回空列表
    if table is None:
        return ["Error"]
    # 提取 TABLE 下所有 a 标签的 href
    table_links = {a["href"] for a in table.find_all("a", href=True)}

    return list(table_links)


# 测试
url_to_scrape = "https://jidian.njfu.edu.cn/szdw/index.html"
links_list = teachers_4(url_to_scrape)
print("提取到的链接列表:", links_list)
