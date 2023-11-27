import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def teacher_3(url):
    links = []  # 存放链接的列表

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"无法访问页面：{url}")
        return links

    soup = BeautifulSoup(response.content, "html.parser")

    # 查找所有符合条件的 <table> 元素
    tables = soup.find_all(
        "table", {"border": "0", "cellpadding": "0", "cellspacing": "0"}
    )

    for table in tables:
        # 找到包含链接的 tr 元素
        for tr in table.find_all("tr"):
            # 找到包含链接的 td 元素
            link_td = tr.find("td", {"height": "26", "align": "center"})
            if link_td:
                link = link_td.find("a")
                if link:
                    href_value = link.get("href")
                    links.append(href_value)

    return links


# 测试
url_to_scrape = [
    "https://hg.njfu.edu.cn//szdw/js/index.html",
    "http://hg.njfu.edu.cn//szdw/js/index.html",
    "http://hg.njfu.edu.cn//szdw/fjs/index.html",
    "http://hg.njfu.edu.cn//szdw/js1335/index.html",
    "http://hg.njfu.edu.cn//szdw/lbry/index.html",
    "http://hg.njfu.edu.cn//szdw/tpjs/index.html",
    "http://hg.njfu.edu.cn//szdw/cyjs/index.html",
]


for url in url_to_scrape:
    links_list = []
    links_list = teacher_3(url)
    print("提取到的链接列表:", links_list)
