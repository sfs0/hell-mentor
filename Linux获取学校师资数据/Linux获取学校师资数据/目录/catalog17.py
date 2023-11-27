import requests
from bs4 import BeautifulSoup
import chardet
from urllib.parse import urljoin


def crawl_webpage(College_website="https://szw.njfu.edu.cn/class_type.asp?id=496"):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        }

        response = requests.get(College_website, headers=headers)

        if response.status_code == 200:
            # 获取网页实际编码

            encoding = chardet.detect(response.content)["encoding"]

            # 使用实际编码解码网页内容，并转换为 UTF-8
            decoded_content = response.content.decode(encoding, "ignore")
            utf8_content = decoded_content.encode("utf-8", "ignore")

            soup = BeautifulSoup(utf8_content, "html.parser")

            # 查找指定 id 的 ul 标签
            target_ul = soup.find("ul", {"id": "nav"})

            # 提取目标 ul 下的所有 li 中的链接
            target_links = []
            if target_ul:
                # 查找所有子 ul 中的所有 li 中的链接
                sub_ul_tags = target_ul.find_all("ul")
                for sub_ul_tag in sub_ul_tags:
                    li_tags = sub_ul_tag.find_all("li")
                    for li_tag in li_tags:
                        a_tag = li_tag.find("a", href=True)
                        if a_tag:
                            href = a_tag["href"]

                            # 将相对链接转换为绝对链接
                            absolute_url = urljoin(College_website, href)

                            # 将 URL 添加到列表
                            target_links.append(absolute_url)

            return target_links
        else:
            print(f"无法获取网页。状态码: {response.status_code}")
            return ["Error"]
    except Exception as e:
        print(f"发生错误: {e}")
        return ["Error"]
