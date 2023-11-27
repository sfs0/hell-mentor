import requests
from bs4 import BeautifulSoup
import chardet


def crawl_webpage(College_website="https://jty.njfu.edu.cn/szdw/index.html"):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        }

        response = requests.get(College_website, headers=headers)

        if response.status_code == 200:
            # 获取网页实际编码
            encoding = chardet.detect(response.content)["encoding"]

            # 使用实际编码解码网页内容，并转换为UTF-8
            decoded_content = response.content.decode(encoding, "ignore")
            utf8_content = decoded_content.encode("utf-8", "ignore")

            soup = BeautifulSoup(utf8_content, "html.parser")

            # 查找第一个符合条件的 table
            target_td = soup.find(
                "table",
                width="90%",
                border="0",
                align="center",
                cellpadding="0",
                cellspacing="0",
            )

            # 提取该 td 下的所有 href
            target_links = []
            if target_td:
                a_tags = target_td.find_all("a", href=True)
                for a_tag in a_tags:
                    href = a_tag["href"]
                    target_links.append(href)

            return target_links
        else:
            print(f"无法获取网页。状态码: {response.status_code}")
            return ["Error"]
    except Exception as e:
        print(f"发生错误: {e}")
        return ["Error"]


print(crawl_webpage())
