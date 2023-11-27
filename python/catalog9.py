import requests
from bs4 import BeautifulSoup
import chardet


def crawl_webpage(College_website="https://yuanlin.njfu.edu.cn/szdw/index.html"):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        }

        response = requests.get(College_website, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 获取网页实际编码
        encoding = chardet.detect(response.content)["encoding"]

        # 使用实际编码解码网页内容，并转换为UTF-8
        decoded_content = response.content.decode(encoding, "ignore")
        utf8_content = decoded_content.encode("utf-8", "ignore")

        # 修改文件写入部分
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(utf8_content.decode("utf-8", "ignore"))

        soup = BeautifulSoup(utf8_content, "html.parser")

        links = set()  # 使用集合存储链接，确保唯一性

        # 通过 :-soup-contains 选择器定位包含 "师资队伍" 文本的元素
        faculty_a = soup.select_one("a:-soup-contains('师资队伍')")
        if faculty_a:
            faculty_li = faculty_a.find_parent("li")

            # 提取师资队伍同级ul下的所有li标签中的href
            faculty_links = {}
            if faculty_li:
                li_tags = faculty_li.select(".nav_sub > li")  # 获取同级的li
                for li_tag in li_tags:
                    a_tag = li_tag.find("a")
                    if a_tag:
                        title = a_tag.get_text(strip=True)
                        href = a_tag["href"]

                        # Check if the li has subcategories
                        sub_ul = li_tag.find("ul", class_="s")
                        if sub_ul:
                            # If yes, extract href from the subcategories
                            sub_links = {
                                sub_a.get_text(strip=True): sub_a["href"]
                                for sub_a in sub_ul.find_all("a")
                            }
                            faculty_links[title] = sub_links
                        else:
                            # If no subcategories, use the href from the main li
                            faculty_links[title] = href

                    # 将链接添加到集合中

                    for title, href in faculty_links.items():
                        if isinstance(href, dict):
                            for sub_title, sub_href in href.items():
                                links.add(sub_href)  # 将链接添加到集合中
                        else:
                            links.add(href)  # 将链接添加到集合中

            else:
                print("未找到师资队伍链接。")

        return list(links)  # 返回链接集合
    except requests.RequestException as e:
        print(f"发生请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


print(crawl_webpage())
