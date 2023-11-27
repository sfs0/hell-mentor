import requests
from bs4 import BeautifulSoup
import chardet


def get_html_encoding(html_content):
    result = chardet.detect(html_content)
    return result["encoding"]


def crawl_webpage(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # 获取网页实际编码
            encoding = get_html_encoding(response.content)

            # 使用实际编码解码网页内容，并转换为UTF-8
            decoded_content = response.content.decode(encoding, "ignore")
            utf8_content = decoded_content.encode("utf-8", "ignore")

            soup = BeautifulSoup(utf8_content, "html.parser")

            # 查找符合条件的 TABLE 标签
            table = soup.find(
                "table",
                {
                    "cellspacing": "1",
                    "cellpadding": "0",
                    "width": "90%",
                    "align": "center",
                    "border": "0",
                    "bgcolor": "#CCCCCC",
                },
            )

            # 提取 TABLE 下所有 a 标签的 href
            table_links = {a["href"] for a in table.find_all("a", href=True)}

            # 将链接写入文件
            with open("table_links.txt", "w", encoding="utf-8") as file:
                for link in table_links:
                    file.write(f"{link}\n")

            print("TABLE下的所有href已成功写入table_links.txt文件。")

            return list(table_links)

        else:
            print(f"无法获取网页。状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None


url_to_crawl = "https://art.njfu.edu.cn/szdw/jsfc/"
result_links = crawl_webpage(url_to_crawl)

if result_links:
    print("去重后的TABLE下的所有href:")
    for link in result_links:
        print(link)
