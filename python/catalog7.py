import requests
from bs4 import BeautifulSoup
import chardet


def crawl_webpage(College_website="http://renwen.njfu.edu.cn/"):
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

            # 查找包含师资队伍链接的div
            menu3_div = soup.find("div", id="menu3")

            # 提取div id为menu3下的所有li标签中的href
            menu3_links = []
            if menu3_div:
                li_tags = menu3_div.select("li")  # 获取下级的li
                for li_tag in li_tags:
                    a_tag = li_tag.find("a")
                    if a_tag:
                        href = a_tag["href"]
                        menu3_links.append(href)

                print("链接已成功写入faculty_links.txt文件。")
            else:
                print("未找到div id为menu3的内容。")

            return menu3_links
        else:
            print(f"无法获取网页。状态码: {response.status_code}")
            return ["Error"]
    except Exception as e:
        print(f"发生错误: {e}")
        return ["Error"]


print(crawl_webpage())
