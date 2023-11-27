import string
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def teachers_3(base_url="https://cem.njfu.edu.cn/szdw.asp"):
    base_url = base_url + "?a=1&page={}"
    page_number = 1
    full_urls = []  # 新建一个空列表

    while page_number <= 7:
        url = base_url.format(page_number)
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"无法访问页面：{url}")
            break

        soup = BeautifulSoup(response.content, "html.parser")
        results_div = soup.find("div", class_="results")

        if results_div:
            for item_div in results_div.find_all("div", class_="item"):
                link_div = item_div.find("div", class_="link")
                href_value = link_div.find("a").get("href")
                full_url = "https://cem.njfu.edu.cn/" + href_value
                full_urls.append(full_url)  # 将每个 full_url 添加到列表中
        else:
            print(f"未找到结果 div，可能已经到达最后一页：{url}")
            break

        page_number += 1

    return full_urls  # 返回包含链接的列表
