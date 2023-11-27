import requests
from bs4 import BeautifulSoup
import chardet
from urllib.parse import urljoin


def get_html_encoding(html_content):
    result = chardet.detect(html_content)
    return result["encoding"]


def crawl_webpage(url, target_id):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # 获取网页实际编码
            encoding = get_html_encoding(response.content)

            # 使用实际编码解码网页内容，并转换为 UTF-8
            decoded_content = response.content.decode(encoding, "ignore")
            utf8_content = decoded_content.encode("utf-8", "ignore")

            # 修改文件写入部分
            with open("output.txt", "w", encoding="utf-8") as file:
                file.write(utf8_content.decode("utf-8", "ignore"))

            soup = BeautifulSoup(utf8_content, "html.parser")

            # 查找指定 id 的 ul 标签
            target_ul = soup.find("ul", {"id": target_id})

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
                            absolute_url = urljoin(url, href)

                            # 将 URL 添加到列表
                            target_links.append(absolute_url)

                # 将链接写入文件
                with open(f"{target_id}_links.txt", "w", encoding="utf-8") as file:
                    for href in target_links:
                        file.write(f"{href}\n")

                print(f"链接已成功写入 {target_id}_links.txt 文件。")

            return soup, target_links
        else:
            print(f"无法获取网页。状态码: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"发生错误: {e}")
        return None, None


def main():
    url_to_crawl = "https://szw.njfu.edu.cn/class_type.asp?id=496"
    target_id = "nav"
    result_soup, result_links = crawl_webpage(url_to_crawl, target_id)

    if result_soup:
        print(f"网页内容已写入 output.txt。")
        print(f"得到的 {target_id} 子 UL 中的 LI 链接:")
        for link in result_links:
            print(link)


if __name__ == "__main__":
    main()
