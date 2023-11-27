from selenium import webdriver
from bs4 import BeautifulSoup
import time


def extract_links_from_dynamic_content(url, output_file):
    # 使用 Chrome 驱动，请确保你的 Chrome 浏览器已安装，并下载对应版本的 ChromeDriver
    driver = webdriver.Chrome()
    driver.get(url)

    # 等待页面加载，这里可以根据实际情况调整等待时间
    time.sleep(5)

    # 获取页面源码
    page_source = driver.page_source

    # 关闭浏览器驱动
    driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")

    # 查找符合条件的 TABLE 标签
    table = soup.find("div", {"id": "ajaxpage-list"})

    # 提取 TABLE 下所有 a 标签的 href
    links = [a.get("href") for a in table.find_all("a", href=True)]
    print(len(links))

    # 存放到文件中
    with open(output_file, "a", encoding="utf-8") as file:
        for link in links:
            file.write(link + "\n")

    print(f"链接列表已保存到文件: {output_file}")
    return links


# 测试
url_to_scrape = [
    "http://renwen.njfu.edu.cn/xkjs/js/index.html",
    "http://renwen.njfu.edu.cn/xkjs/fjs/index.html",
    "http://renwen.njfu.edu.cn/xkjs/js1/index.html",
]

# 指定保存所有链接的文件名
all_links_file = "all_links.txt"

for url in url_to_scrape:
    links_list = extract_links_from_dynamic_content(url, all_links_file)
    print("提取到的链接列表:", links_list)
    print("=" * 50)
