import re
import string
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def institution_3(College_website:string):
    response = requests.get(College_website,headers=headers)
    html_content = response.content.decode('utf-8')# 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    teacher_category = []
    try:
        matching_table = soup.find('table',id='left')
        
        child_tr_tags = [child for child in matching_table.contents if child.name == 'tr']
        
        second_tr = child_tr_tags[1]
        #print(second_tr)
        all_links = second_tr.find_all('a')
        
        for link in all_links:
            teacher_category.append(link.get('href'))
        teacher_category = teacher_category[:-3]
        return teacher_category
    except Exception:
        return ["Error"]


# def institution_4(College_website:string):
    # response = requests.get(College_website,headers=headers)
    # html_content = response.content.decode('utf-8')# 使用BeautifulSoup解析HTML
    # if response.status_code != 200:
    #     print(f"无法获取网页。状态码: {response.status_code}")
    #     return ["Error"]
    # # 获取网页实际编码
    # soup = BeautifulSoup(html_content, 'html.parser')
    # faculty_links = []
    # faculty_div = soup.find("a", string="师资队伍").find_next("div", {"id": "m5"})
    # a_tags = faculty_div.find_all("a")
    # for a_tag in a_tags:
    #     href = a_tag["href"]
    #     faculty_links.append(href)
        
    # if faculty_links:
    #     #faculty_links = faculty_links[1:]#移除第一个元素，因为特聘教授里面没有任何东西
    #     return faculty_links
    # else:
    #     return ["Error"]
    
        
def institution_7(College_website:string):
    # response = requests.get(College_website, headers=headers)

    # if response.status_code == 200:
    #     response = requests.get(College_website,headers=headers)
    #     html_content = response.content.decode('utf-8')# 使用BeautifulSoup解析HTML
    #     soup = BeautifulSoup(html_content, 'html.parser')
        
    #     menu3_div = soup.find("div", id="menu3")# 查找包含师资队伍链接的div
    #     menu3_links = []# 提取div id为menu3下的所有li标签中的href
    #     if menu3_div:
    #         li_tags = menu3_div.select("li")  # 获取下级的li
    #         for li_tag in li_tags:
    #             a_tag = li_tag.find("a")
    #             if a_tag:
    #                 href = a_tag["href"]
    #                 menu3_links.append(href)
    #     return menu3_links
    # else:
    #     print(f"无法获取网页。状态码: {response.status_code}")
    #    return ["Error"]
    pass
                

def institution_8(College_website:string):
    response = requests.get(College_website,headers=headers)
    html_content = response.content.decode('utf-8')# 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    teacher_category = []
    div = soup.find('div', id="m4")
    if div:
        a_tags = div.find_all('a')
        for a in a_tags:
            href = a.get('href')  # 获取 <a> 标签的 href 属性值
            teacher_category.append(href)
    return teacher_category


def institution_9(College_website:string):
    response = requests.get(College_website,headers=headers)
    html_content = response.content.decode('utf-8')# 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    links = set()  # 使用集合存储链接，确保唯一性
    # 通过 :-soup-contains 选择器定位包含 "师资队伍" 文本的元素
    faculty_a = soup.select_one("a:-soup-contains('师资队伍')")
    faculty_li = faculty_a.find_parent("li")
    faculty_links = {}# 提取师资队伍同级ul下的所有li标签中的href
    if faculty_li:
        li_tags = faculty_li.select(".nav_sub > li")  # 获取同级的li
        for li_tag in li_tags:
            a_tag = li_tag.find("a")
            if a_tag:
                title = a_tag.get_text(strip=True)
                href = a_tag["href"]
                sub_ul = li_tag.find("ul", class_="s")  # Check if the li has subcategories
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

            for title, href in faculty_links.items():# 将链接添加到集合中
                if isinstance(href, dict):
                    for sub_title, sub_href in href.items():
                        links.add(sub_href)  # 将链接添加到集合中
                else:
                    links.add(href)  # 将链接添加到集合中
    return links  # 返回soup和链接集合


def institution_17(College_website:string):
    response = requests.get(College_website,headers=headers)
    html_content = response.content.decode('gb2312')# 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    return ["Error"]
    # print(soup.prettify())
    # exit()
    # target_ul = soup.find('ul',id = 'nav')# 查找指定 id 的 ul 标签
    # target_links = []# 提取目标 ul 下的所有 li 中的链接
    # if target_ul:#没找到！
    #     sub_ul_tag = target_ul.find('ul')# 查找所有子 ul 中的所有 li 中的链接
    #     li_tag = sub_ul_tag.find_all('li')
    #     a_tags = li_tag.find_all('a')
    #     if a_tags:
    #         for a_tag in a_tags:
    #             href = "https://szw.njfu.edu.cn/" + a_tag["href"]
    #             target_links.append(href)# 将 URL 添加到列表
    #     return target_links
    # else:
    #     return ["Error"]

def no_category(College_website:string):
    return [College_website]

def generic_func(College_website:string): #                     7个学院通用函数
    #college_url="https://it.njfu.edu.cn/"
    response = requests.get(College_website,headers=headers)
    html_content = response.content.decode('utf-8')# 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    Group_Of_teachers = "师资队伍"
    teacher_category = []
    
    for tag in soup.find_all(text=True):#去除掉多余的空白符
        new_text = re.sub(r'\s+', '', tag)
        tag.replace_with(new_text)

    target = soup.find(text=Group_Of_teachers)
    print(target)
    if target:
        target_tag = target.parent.parent# 获取所有<a>标签里的href链接
        if target_tag:
            links = target_tag.find_all('a', href=True)
            for link in links:
                teacher_category.append(link['href'])
        del teacher_category[0]#删去第一个a标签，因为第一个a标签多半是索引，是无效的
        #-----------------------------------------
        return teacher_category
    else:
        return ["Error"]


function_map = {
'institution_1': generic_func,
'institution_2': generic_func,
'institution_3': institution_3,
'institution_4': no_category,
'institution_5': generic_func,
'institution_6': no_category,
'institution_7': no_category,
'institution_8': institution_8,
'institution_9': institution_9,
'institution_10': no_category,
'institution_11': no_category,
'institution_12': no_category,
'institution_13': no_category,
'institution_14': no_category,
'institution_15': no_category,
'institution_16': no_category,
'institution_17': institution_17,
'institution_18': no_category,
}


def call_function(function_name, url):
    # 根据传入的参数调用相应的函数
    if function_name in function_map:
        result = function_map[function_name](url)
        return result
    else:
        return ["Error"]

def get_category(College_id:int,url:string):
    result = call_function("institution_"+str(College_id),url)
    if result==["Error"]:
        print("找不到links")
        exit(1)
    else:
        return result

