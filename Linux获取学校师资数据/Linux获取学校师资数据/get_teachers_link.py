import string
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def call_function(function_name, url):
    # 根据传入的参数调用相应的函数
    function_map = {
        f"teachers_{i}": globals()[f"teachers_{i}"] for i in range(1, 19)
    }  #      这里定义了调用对应的函数

    if function_name in function_map:
        result = function_map[function_name](url)
        return result
    else:
        return ["Error"]


# ------------------------------------------------------------------------------------------------------------------------------


def teacher_links(College_id: int, url: string):
    result = call_function("teachers_" + str(College_id), url)
    if result == ["Error"]:
        print("找不到links")
        exit(1)
    else:
        return result


def teachers_1(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [a["href"] for a in soup.select(".teacher-list-con a")]
    return links


def teachers_2(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = []
    results_div = soup.find("div", {"class": "results"})
    result_divs = results_div.find_all("div", {"class": "result"})
    for result_div in result_divs:
        name_divs = result_div.find_all("div", {"class": "names"})
        for div in name_divs:
            a_tags = div.find_all("a")
            for a in a_tags:
                href = a.get("href")
                if href:  # 确保 href 存在
                    links.append(href)
    return links


def teachers_3(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    response = requests.get(url, headers=headers)
    links = []
    if response.status_code != 200:
        print(f"无法访问页面：{url}")
        return ["Error"]
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
    return list(set(links))


def teachers_4(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    # 查找符合条件的 TABLE 标签
    table = soup.find(
        "table",
        {
            "cellspacing": "1",
            "cellpadding": "0",
            "width": "96%",
            "align": "center",
            "border": "0",
            "bgcolor": "#CCCCCC",
        },
    )
    # 安全检查，如果没有找到符合条件的 table，则返回空列表
    if table is None:
        return ["Error"]
    # 提取 TABLE 下所有 a 标签的 href
    table_links = {a["href"] for a in table.find_all("a", href=True)}
    return list(table_links)


def teachers_5(url):
    if url == "https://tumu.njfu.edu.cn//szdw/msdw/index.html":  # 剔除名师队伍这个目录，因为没有有效信息
        return ["Error"]
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    td_list = soup.find(
        "td",
        attrs={
            "width": "auto",
            "bgcolor": "white",
            "style": "padding-left:45px;padding-top:30px;padding-bottom:50px;",
            "align": "left",
            "valign": "top",
        },
    )
    a_tags = td_list.find_all("a")
    if a_tags:
        links = []
        for a_tag in a_tags:
            link = a_tag.get("href")
            links.append(link)
        return links
    else:
        return ["Error"]


def teachers_6(url):
    url = url + "?a=1&page={}"
    page_number = 1
    full_urls = []  # 新建一个空列表

    while page_number <= 7:
        _url = url.format(page_number)
        response = requests.get(_url, headers=headers)

        if response.status_code != 200:
            print(f"无法访问页面：{_url}")
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
            print(f"未找到结果 div，可能已经到达最后一页：{_url}")
            break

        page_number += 1

    return full_urls  # 返回包含链接的列表


def teachers_7(url):  #  文档————————————————————————————
    # print(url)
    file_path = "" + url  # 实际文件路径,记得替换为相对路径！
    result = []
    try:
        with open(file_path, "r") as file:
            result = file.readlines()  # 逐行读取内容并存储在一个列表中
        return result
    except Exception:
        return ["Error"]


def teachers_8(url):
    # print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    result = [
        a["href"] for a in soup.select('tbody tr td[align="center"][valign="middle"] a')
    ]
    return result


def teachers_9(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    # 查找所有符合条件的 TABLE 标签
    tables = soup.find_all(
        "table",
        {
            "cellspacing": "1",
            "cellpadding": "0",
            "width": "96%",
            "align": "center",
            "border": "0",
            "bgcolor": "#cccccc",
        },
    )

    links = []
    # 遍历每个符合条件的表格，提取链接
    for table in tables:
        links.extend([a.get("href") for a in table.find_all("a", href=True)])

    return list(set(links))  # 返回去重后的链接列表


def teachers_10(url):  #  文档————————————————————————————————————————————
    return teachers_7(url)


def teachers_11(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    # 找到符合条件的 <td> 标签
    td_tag = soup.find("td", {"colspan": "2", "valign": "top"})
    # 找到 <a> 标签并提取 href 属性
    links = [a.get("href") for a in td_tag.find_all("a", href=True)]

    return list(set(links))  # 去重并返回


def teachers_12(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")  # 查找符合条件的 TABLE 标签
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
    if table:
        table_links = {
            a["href"] for a in table.find_all("a", href=True)
        }  # 提取 TABLE 下所有 a 标签的 href
        return list(table_links)
    else:
        return ["Error"]


def teachers_13(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    # 查找符合条件的 TABLE 标签
    tables = soup.find_all(
        "table",
        {
            "cellspacing": "1",
            "cellpadding": "0",
            "width": "100%",
            "align": "center",
            "border": "0",
        },
    )
    links = []
    for table in tables:  # 提取 TABLE 下所有 a 标签的 href
        links.extend([a.get("href") for a in table.find_all("a", href=True)])
    return links


def teachers_14(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    target_td = soup.find("td", colspan="2", valign="top")  # 查找第一个符合条件的 table
    target_links = []
    if target_td:
        a_tags = target_td.find_all("a", href=True)
        for a_tag in a_tags:  # 提取该 td 下的所有 href
            href = a_tag["href"]
            target_links.append(href)
        return target_links
    else:
        return ["Error"]


def teachers_15(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    target_td = soup.find(
        "table",
        width="90%",
        border="0",
        align="center",
        cellpadding="0",
        cellspacing="0",
    )  # 查找第一个符合条件的 table
    target_links = []
    if target_td:
        a_tags = target_td.find_all("a", href=True)
        for a_tag in a_tags:  # 提取该 td 下的所有 href
            href = a_tag["href"]
            target_links.append(href)
        return target_links
    else:
        return ["Error"]


def teachers_16(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    if response.status_code != 200:
        print(f"无法访问页面：{url}")
        return []
    # 查找符合条件的 TABLE 标签
    tables = soup.find_all(
        "table",
        {
            "cellspacing": "1",
            "cellpadding": "0",
            "width": "100%",
            "align": "center",
            "border": "0",
        },
    )

    # 提取 TABLE 下所有 a 标签的 href
    links = []
    for table in tables:
        links.extend([a.get("href") for a in table.find_all("a", href=True)])

    return links


def teachers_17(url):  # 放着看情况
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")


def teachers_18(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    target_td = soup.find(
        "table", border="0", cellpadding="0", cellspacing="0", width="100%"
    )  # 查找第一个符合条件的 table
    target_links = []
    if target_td:
        a_tags = target_td.find_all("a", href=True)
        for a_tag in a_tags:  # 提取该 td 下的所有 href
            href = a_tag["href"]
            target_links.append(href)
        return target_links
    else:
        return ["Error"]
