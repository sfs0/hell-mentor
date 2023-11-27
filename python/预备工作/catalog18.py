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

            # 修改文件写入部分
            with open("output.txt", "w", encoding="utf-8") as file:
                file.write(utf8_content.decode("utf-8", "ignore"))

            soup = BeautifulSoup(utf8_content, "html.parser")

            # 查找第一个符合条件的 table
            target_td = soup.find(
                "table", border="0", cellpadding="0", cellspacing="0", width="100%"
            )

            # 提取该 td 下的所有 href
            target_links = []
            if target_td:
                a_tags = target_td.find_all("a", href=True)
                for a_tag in a_tags:
                    href = a_tag["href"]
                    target_links.append(href)

                # 将链接写入文件
                with open("td_links.txt", "w", encoding="utf-8") as file:
                    for href in target_links:
                        file.write(f"{href}\n")

                print("链接已成功写入td_links.txt文件。")

            return soup, target_links
        else:
            print(f"无法获取网页。状态码: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"发生错误: {e}")
        return None, None


url_to_crawl = "https://sky.njfu.edu.cn/szdw/index.html"
result_soup, result_links = crawl_webpage(url_to_crawl)

if result_soup:
    print(f"网页内容已写入output.txt。")
    print("得到的链接:")
    for link in result_links:
        print(link)
