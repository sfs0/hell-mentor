import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def find_links_in_table(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # 查找所有符合条件的 TABLE 标签
    tables = soup.find_all(
        "table",
        {
            "cellspacing": "1",
            "cellpadding": "0",
            "width": "96%",
            "align": "center",
            "border": "0",
            "bgcolor": "#cccccc",
        },
    )

    links = []
    # 遍历每个符合条件的表格，提取链接
    for table in tables:
        links.extend([a.get("href") for a in table.find_all("a", href=True)])

    return list(set(links))  # 返回去重后的链接列表


link = [
    "http://yuanlin.njfu.edu.cn/szdw/zyjs/ylzwx/index.html",
    "http://yuanlin.njfu.edu.cn/szdw/zyjs/fjylghx/index.html",
    "http://yuanlin.njfu.edu.cn/szdw/zyjs/cssjx/index.html",
    "http://yuanlin.njfu.edu.cn/szdw/zyjs/jgjzx/index.html",
    "http://yuanlin.njfu.edu.cn/szdw/zyjs/cxghx/index.html",
]

for url in link:
    print("教师链接：")
    ans = find_links_in_table(url)
    print(ans)
