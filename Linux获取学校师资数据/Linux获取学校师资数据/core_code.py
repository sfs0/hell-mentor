from ast import keyword
from logging import exception
import re
from turtle import title
from unicodedata import name
from unittest import skip
from bs4 import NavigableString
import requests
from bs4 import BeautifulSoup
import attributes
import string
import json
import os


class main_code:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"}
    translation = attributes.get_translation()


    def __init__(self , url ,id:string ,base_path , College_website:string ,College_id) -> None:
        self.data = attributes.get_initialize_data()
        self.key_words = attributes.get_keywords()
        self.url=url.strip()
        self.name = None
        self.person_id=id
        self.base_path=base_path
        self.College_website = College_website
        self.College_id = College_id
        self.Brief_version = attributes.get_brief_info()#单独拉一个略缩版的出来
        
        # if self.url.startswith("http://"):
        #     self.url = "https://" + self.url[len("http://"):]
        response = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(response.content, 'html.parser')

    def tackle(self):#初始化本类的时候用的学院id是多少，就自动调用相应的函数
        self.func = {i: getattr(self, f'institution_{i}') for i in range(1, 19)}
        return self.func[int(self.College_id)]()

    def down_load(self):
        final_path=self.base_path + "news/" + self.College_id + "/"#下载位置
        if not os.path.exists(final_path):
            os.makedirs(final_path)
        with open(final_path + self.person_id +'.json','w',encoding='utf-8') as file:
            json.dump(self.data,file, ensure_ascii=False,indent=4)

        # if self.data["Paper"] != "None" and self.data["Achievements"] !="None":
        #     print(str(self.College_id)+"学院存在这个问题")
            
        print(str(self.person_id) + "下载成功！")

    def get_brief(self):
        self.data["id"] = self.person_id
        self.Brief_version["id"]=self.data["id"]
        self.Brief_version["Name"]=self.data["Name"]
        self.Brief_version["Research_direction"]=self.data["Research_direction"]
        self.Brief_version["img"]=self.data["img"]




    def institution_1(self):
        #------------------------------------作用域为  teacher-top---------------------------------------
        head_div = self.soup.find('div', {'class': 'teacher-top'})
        #div_tags = head_div.find_all('div')
        #-------获取照片的部分-------
        if head_div is not None:
            img_div = head_div.find('div', {'class': 'head-pic'})
            img = img_div.find('img')
        else:
            print("page is None,"+self.url)
            return ["Error"]

        if img:#获得教师照片
            self.data['img'] = self.College_website + img.get('src')
        #-------获取姓名部分--------
        name = None
        list_name_div = self.soup.select('.head-info-list-name')# 使用 CSS 选择器找到第一个 "姓名" 标签
        if list_name_div[0]:#获取到基本信息栏
            name_value_div = list_name_div[0].find_next_sibling('div')# 使用 next_sibling 属性找到与 "姓名" 标签同级别的下一个 div 标签
            name = name_value_div.get_text(strip=True)
            self.data["Name"]=name
            self.data["id"]=self.person_id
        #--------获取其他小信息部分--------
        list_title_div = self.soup.select('.head-info-list-title')
        for i in range(1,len(list_title_div)):
            key=list_name_div[i].get_text().strip()
            value=list_title_div[i].get_text().strip()

            for _keyword in self.key_words:
                if _keyword in key:
                    if self.data[self.translation[_keyword]] == "None":
                        self.data[self.translation[_keyword]] = ""
                    self.data[self.translation[_keyword]] += value

        body_info = self.soup.find('div',{'class':'teacher-bottom'})
        # p_tags = body_info.find_all('p')
        divs = body_info.find_all('div',{'class':'teacher-bottom-list'})
        for div in divs:
            small_divs = div.find_all('div')
            title_text = small_divs[0].get_text().strip()
            ps = small_divs[1].find_all('p')
            _now_keyword = None

            for key_word in self.key_words:#找到关键词就跳过，准备下一次的写入内容
                    if key_word in title_text:
                        _now_keyword = key_word

            for p in ps:#还是要把内容的每个p标签都找一遍
                content_text = p.get_text().strip()
                skip = False

                #------------------给某老师开特例----------------------
                if name == "冯渊圆" and _now_keyword == '研究方向' and len(content_text)>45:
                    skip = True
                    break
                if name == "曹林" and _now_keyword == '研究方向':
                    _now_keyword = "简介"
                if name == "郭起荣" and _now_keyword == '研究方向' and content_text == "【专长课程】":
                    skip = True
                    break
                #-----------------------------------------------------

                if skip == True:
                    break
                elif _now_keyword != None:
                    if self.data[self.translation[_now_keyword]] =="None":
                        self.data[self.translation[_now_keyword]] = content_text
                    else:
                        self.data[self.translation[_now_keyword]] += content_text + "<br/>"


        #----------------------------------------------------------------------------------------------
        self.down_load()
        self.get_brief()
        return self.Brief_version

        
    def institution_2(self):
        teacher_div = self.soup.find('div',{'class':'container teacher'})
        if not teacher_div:
            print("Page is None! "+self.url)
            return ["Error"]

        intro_div = teacher_div.find('div',{'class':'teacher-intro'})
        if teacher_div is not None:
            if intro_div is not None:
                img = intro_div.find('img')
        else:
            print("page is None,"+self.url)
            self.get_brief()
            return self.Brief_version

        if img:#获得教师照片
            self.data['img'] = self.College_website + img.get('src')
        #---------------------------------获得姓名-------------------------------------------------
        name = None
        name_div = intro_div.find('div',{'class':'name'})
        name = name_div.contents[0].strip()
        self.data["Name"] = name
        self.data["id"]=self.person_id
        #---------------------------------获得小信息--------------------------------------
        small_info = intro_div.find('div',{'class':'link'})
        span_tags = small_info.find_all('span')
        for span in span_tags:
            span_info = span.get_text().strip()
            for key_word in self.key_words:
                if key_word in span_info and span_info.replace(key_word+":","")!="":
                    # print(name +"   "+ key_word)
                    # exit()
                    self.data[self.translation[key_word]] = span_info.replace(key_word+":","")
        #-------------------------------更多信息------------------------------------------
        achievement_divs = teacher_div.find_all('div',{'class':'achievement'})
        for achievement_div in achievement_divs:
            title_div = achievement_div.find('div',{'class':'achievement-title'})
            title = title_div.get_text(strip=True)
            now_keyword = None
            for key_word in self.key_words:
                if key_word in title:
                    now_keyword = key_word
            
            if now_keyword == None:
                break

            p_tags = achievement_div.find_all('p')
            content = ""
            for p in p_tags:
                if now_keyword == "项目" or now_keyword == "论文":
                    content += p.get_text() + "   "
                else:
                    content += p.get_text() + "<br/>"
            self.data[self.translation[now_keyword]] = content
        #----------------------------------------------------------------------------------------------
        self.down_load()
        self.get_brief()
        return self.Brief_version
    
    def institution_3(self):
        #------------------------------获得姓名-----------------------------------------
        name_span = self.soup.select('span[style="padding-left:10px; font-family:\'微软雅黑\'; font-size:16px; color:#ffffff;"]')
        if name_span:
            self.data["Name"] = name_span[0].text.strip()#获得姓名以及拼音
        else:
            return ["Error"]
        #------------------------------获得照片-----------------------------------------
        img_p = self.soup.find('p', attrs={'align': 'center'})
        img = img_p.find('img')
        if img:
            if img.get('src')!="/DFS//file/2020/06/23/20200623154141680f55n45.jpg?iid=47622":
                self.data["img"] = "https://hg.njfu.edu.cn" + img.get('src')
        #------------------------------获得小信息-----------------------------------------
        small_info_table = self.soup.find('table', attrs={'width': "90%", 'border': "0", 'align': "center", 'cellpadding': "0", 'cellspacing': "0"})
        span_tags = small_info_table.find_all('span')
        for span in span_tags:
            span_text = span.get_text().strip()
            for key_word in self.key_words:
                if key_word in span_text:
                    if self.data[self.translation[key_word]] == "None":
                        self.data[self.translation[key_word]] = ""
                    self.data[self.translation[key_word]] += span_text.replace(key_word + "：","")
        #------------------------------获得大信息-----------------------------------------
        #td_tag = self.soup.find('td', attrs={'width': "799", 'valign': "top"})
        more_info_table = self.soup.find()
        big_table = more_info_table.find('table', attrs={'width': '90%', 'height': '48', 'border': '0', 'align': 'center', 'cellpadding': '0', 'cellspacing': '0'})
        diff_tables = big_table.find_all('table')[1:6]
        for diff_table in diff_tables:
            trs = diff_table.find_all('tr')

            now_keyword = None
            for tr in trs:
                
                tr_text = tr.get_text(strip=True)
                if tr_text == "":
                    continue

                if now_keyword == None:
                    for keyword in self.key_words:
                        if keyword in tr_text:
                            now_keyword = keyword
                            break
                else:
                    ps = tr.find_all('p')
                    for p in ps:
                        p_content = p.get_text().strip()
                        if p_content == "":
                            continue
                        if self.data[self.translation[now_keyword]] == "None":
                            self.data[self.translation[now_keyword]] = ""
                        self.data[self.translation[now_keyword]] += p_content + "<br/>"
                    now_keyword = None

        self.down_load()
        self.get_brief()
        #-------------------给某老师开特例---------------------
        if "徐勇" in self.data["Name"]:
            self.Brief_version["Research_direction"] = self.Brief_version["Research_direction"][:233]
        #-----------------------------------------------------
        return self.Brief_version
        

    def institution_4(self):      #有提升空间
        info_table = self.soup.find('table', attrs={'width': "96%", 'height': "48", 'border': "0", 'align': "center", 'cellpadding': "0", 'cellspacing': "0"})
        #------------------------------获得姓名-----------------------------------------
        name_td = self.soup.find('td', text='姓名：')
        name = name_td.find_next_sibling('td').get_text().strip()
        if not name:
            return ["Error"]
        self.data["Name"] = name
        #------------------------------获得照片-----------------------------------------
        img_tag = info_table.find('img')
        if img_tag:
            if img_tag.get('src') != "/DFS//file/2020/06/23/20200623154141680f55n45.jpg?iid=36676":
                self.data["img"] = "https://jidian.njfu.edu.cn" + img_tag.get('src')
        #------------------------------获得小信息-----------------------------------------
        small_info_table = info_table.find_all('table', attrs={'cellspacing': "1", 'cellpadding': "0", 'width': "100%", 'align': "center", 'border': "0", 'bgcolor': "#CCCCCC"})
        #  ↑这里是拿到小表格
        tr_tags = small_info_table[0].find_all('tr')
        for tr in tr_tags:
            tds = tr.find_all('td')
            if len(tds) == 4:
                label1 = (tds[0].get_text().strip())[:-1]
                value1 = tds[1].get_text().strip()
                label2 = (tds[0].get_text().strip())[:-1]
                value2 = tds[1].get_text().strip()
                if label1 in self.key_words and value1!="":
                    self.data[self.translation[label1]] = value1
                if label2 in self.key_words and value2!="":
                    self.data[self.translation[label2]] = value2
            else:
                continue
        #------------------------------获得大信息-----------------------------------------
        otherInfo_table = small_info_table[1]
        if otherInfo_table:
            tr_tags = otherInfo_table.find_all('tr')
            now_title = None
            for tr_tag in tr_tags:
                content = tr_tag.get_text(strip=True)  # 获取标题
                
                if now_title == None:
                    if len(content)>12:
                        content = content[:12]#这里截取的是标题，随便截取，别担心
                    for key_word in self.key_words:
                        if key_word in content:
                            now_title = key_word
                    continue
                else:#下面才是获取正文的部分
                    if self.data[self.translation[now_title]] == "None":#如果还没有放过数据，就先清空
                        self.data[self.translation[now_title]] = ""

                    if now_title == "项目":
                        self.data[self.translation[now_title]] = content
                    else:
                        ps = tr_tag.find_all('p')
                        for p in ps[1:]:
                            p_content = p.get_text().strip()
                            if p_content != "":
                                self.data[self.translation[now_title]] += p_content + "<br/>"
                                
                    now_title = None
                    continue
                    
        self.get_brief()
        self.down_load()
        return self.Brief_version
    
    def institution_5(self):
        main_td = self.soup.find('td', id="mainPanel")
        if not main_td:#出错检测
            return ["Error"]
        self.data["Name"] = main_td.find_all('div')[1].get_text()
        #------------------------------获得姓名-----------------------------------------
        #div_tags = main_td.find_all('div', recursive=False)
        #------------------------------个人信息-----------------------------------------
        zoom_div = self.soup.find('div', id = 'zoom')
        img = zoom_div.find('img')#----------拿到照片----------
        if img:
            self.data["img"] = self.College_website + img.get('src')
        
        p_tags = zoom_div.find_all('p')
        now_keyword = None
        for p in p_tags:
            p_content = p.get_text(strip=True)

            if p_content == "":
                continue

            content_head = p_content
            if len(p_content)>12:
                content_head = content_head[:12]

            skip = False
            for key_word in self.key_words:
                if key_word in content_head:
                    now_keyword = key_word
                    if len(p_content)<16:
                        skip = True
                    break
            if skip == True or now_keyword == None:
                continue
            
            if self.data[self.translation[now_keyword]] == "None":
                self.data[self.translation[now_keyword]] = p_content
            else:
                self.data[self.translation[now_keyword]] += "<br/>" + p_content

        self.get_brief()
        self.down_load()
        return self.Brief_version


    def institution_6(self):
        teacher = self.soup.find('div',{'class':'teacher'})
        teacher_divs = teacher.find_all('div')
        #------------------获取小信息----------------
        base_info = teacher_divs[0]#第一个是小信息
        img_tag = base_info.find('img')
        if img_tag:
            self.data["img"] = "https://cem.njfu.edu.cn" + img_tag['src']

        info_right = base_info.find('div',{'class':'info-right'})
        info_divs = info_right.find_all('div')
        span = info_divs[0].find('span').text
        self.data["Name"] = info_divs[0].get_text().replace(span,"")

        for info_div in info_divs[1:]:
            if info_div:
                label_text = info_div.label.get_text(strip=True)# 获取title
                span_text = info_div.span.get_text(strip=True)# 获取title相应的内容

                for key_word in self.key_words:
                    if key_word in label_text and span_text != "":
                        if self.data[self.translation[key_word]] == "None":
                            self.data[self.translation[key_word]] = ""
                        self.data[self.translation[key_word]] += span_text
            else:
                print("未能获取到小信息")
                exit()
        #------------------获取大信息----------------
        block_divs = teacher.find_all('div',{'class':'block'})
        for block in block_divs:
            title = block.find('div',{'class':'block-title'}).get_text().strip()
            content = block.find('div',{'class':'fields'})
            content_ps = content.find_all('p')
            now_keyword = None
            for key_word in self.key_words:
                if key_word in title:
                    now_keyword = key_word
                    break
            
            if now_keyword!= None:
                for content_p in content_ps[1:]:
                    p_text = content_p.get_text().strip().replace('\n',"").replace('\r',"")
                    if self.data[self.translation[key_word]] == "None":
                        self.data[self.translation[key_word]] = ""
                    self.data[self.translation[key_word]] += p_text + "<br/>"

                    if self.data["Name"] == "蔡传晰" and key_word == "论文":
                        self.data[self.translation[key_word]] = content_ps[0].get_text()
                        

        self.get_brief()
        self.down_load()
        return self.Brief_version
    
    def institution_7(self):
        #print(self.url)
        name = self.soup.find('span', style="font-size:24px; font-weight:bold").text.strip()
        self.data["Name"] = name
        info_div = self.soup.find('div',id = 'zoom')
        img = info_div.find('img')
        if img:
            self.data["img"] = "https://renwen.njfu.edu.cn" + img['src']
        self.data["Introduction"] = info_div.get_text().strip()
        self.get_brief()
        self.down_load()
        return self.Brief_version
    
    def institution_8(self):#-------------------获取教师信息----------------
        name_table =self.soup.find('table', {'width': '850', 'height': '587', 'border': '0', 'align': 'center', 'cellpadding': '0', 'cellspacing': '0', 'id': '__01'})
        name = name_table.find('h1', {'style': 'font-size:20px'}).text
        self.data["Name"]=name
        #--------------------------------------------------------------------
        self.key_words.insert(0,name)
        self.translation[name] = "Introduction"#把姓名放进keyword中
        #-----------------------------------------------------
        div_element = self.soup.find('div', id="zoom")

        img_tags = div_element.find('img')#找图片
        if img_tags:
            self.data["img"] = self.College_website + img_tags['src']
        #----------------------------------------------------------------------
        now_word = name
        content = ""
        p_tags = div_element.find_all('p')

        now_word=None
        for p_tag in p_tags:#在找到的许多<p>标签里找每个<p>标签的文本内容
            content = p_tag.text.strip()
            #is_find=False#用于判断是否有关键词，没有关键词就是上一次关键词的补充标签
            content_head = content
            if len(content)>16:#避免出现栈的问题
                content_head = content[:16]

            for key_word in self.key_words:
                if key_word in content_head:#只需要查找字符串头，不然容易出现错误
                    #----------------------------------------
                    now_word = key_word
                    if len(content)<16:
                        continue

            if now_word!=None:
                #-------------------特例区----------------------
                if now_word == "研究方向":
                    index = content.find("。")  # 查找第一个句号的索引位置
                    if index != -1:  # 如果找到了句号
                        content = content[:index+1]  # 截取到第一个句号（包括句号）
                    if name == "胡春华":
                        self.data[self.translation[now_word]] = content
                        now_word = "论文"
                        continue
                #----------------------------------------------
                if self.data[self.translation[now_word]]=="None":
                    self.data[self.translation[now_word]] = content
                else:
                    self.data[self.translation[now_word]]+="<br/>" + content
                    
                if now_word == name:#找到带姓名的简介后就移除
                    self.key_words.remove(name)
                    now_word = None
        #file=open('/teacher_info/'+teacher_id+'.txt','w',encoding='utf-8')   #下载到相对目录
        self.get_brief()
        self.down_load()

        return self.Brief_version
        
    def institution_9(self):
        table_tag = self.soup.find('table', id = 'list_right')
        small_info = table_tag.find('table', attrs={'cellspacing': '1', 'cellpadding': '0', 'width': '100%', 'align': 'center', 'border': '0', 'bgcolor': '#cccccc'})
        #---------------------获取基本信息--------------------------
        img = small_info.find('img')
        if img:
            self.data["img"] = self.College_website + img['src']

        tr_tags = small_info.find_all('tr')
        for tr in tr_tags:
            tds = tr.find_all('td')
            now_keyword = None
            for td in tds:
                content = td.get_text().strip()
                if now_keyword == None:
                    for key_word in self.key_words:
                        if key_word in content:
                            now_keyword = key_word
                            break
                else:
                    if self.data[self.translation[now_keyword]] == "None":
                        self.data[self.translation[now_keyword]] = ""
                    self.data[self.translation[now_keyword]] += content
                    now_keyword = None
        #---------------------获取大信息--------------------------
        more_info = table_tag.find('table', attrs={'cellspacing': '1', 'cellpadding': '0', 'width': '100%', 'align': 'center', 'border': '0', 'bgcolor': '#e4cbe8'})
        more_trs = more_info.find_all('tr')
        
        for tr in more_trs:
            if self.data["Research_direction"] == "found":
                research_p = tr.find_all('p')
                filtered_ps = [p for p in research_p if p.get_text(strip=True)]
                if len(filtered_ps)>7:
                    for res_p in filtered_ps:
                        p_content=res_p.get_text().strip()
                        if len(p_content)<16:
                            if self.data["Research_direction"] == "None" or self.data["Research_direction"] == "found":
                                self.data["Research_direction"] = ""
                            self.data["Research_direction"] += p_content+"  "
                else:
                    self.data["Research_direction"] = tr.get_text().strip()
            elif "研究方向" in tr.get_text():
                self.data["Research_direction"] = "found"
        
        for more_tr in more_trs:
            p_tags = more_tr.find_all('p')
            _keyword = None
            for p in p_tags:
                content = p.text
                skip = False
                if len(content)<16:
                    for keyword in self.key_words:#注意这个keyword不要和上面获取小信息的key_word搞混淆了
                        if keyword in content:
                            _keyword = keyword
                            skip = True
                            break
                if _keyword != None and skip == False:
                    if self.data[self.translation[_keyword]] == "None":
                        self.data[self.translation[_keyword]] = ""
                    else:
                        self.data[self.translation[_keyword]] += "<br/>" + content


        self.get_brief()
        self.down_load()
        return self.Brief_version
    
    def institution_10(self):
        #---------------------------------------
        small_info = self.soup.find('div',{'class':'top clearfix'})
        img = small_info.find('img')
        if img:
            self.data["img"] = "https://cos.njfu.edu.cn" + img['src']
        
        small_tables = small_info.find_all('table', attrs={'width': '100%', 'border': '0', 'cellspacing': '0', 'cellpadding': '0', 'class': 'wp_article_list_table'})[1]
    
        h1_tag = small_tables.find('h1', class_='news_title')
        name = ''.join(h1_tag.find_all(text=True, recursive=False)).strip()
        self.data["Name"] = name
        
        small_ps = small_tables.find_all('p')
        for small_p in small_ps:
            small_p_content = small_p.get_text().strip()
            for key_word in self.key_words:
                if key_word in small_p_content:
                    self.data[self.translation[key_word]] = small_p_content[5:]
        
        #-------------------------------------------
        more_info = self.soup.find('div',{'class':'mainbox2'})
        info_divs = more_info.find_all('div', attrs={'class': 'maincon', 'style': False, 'id': False})
        for info_div in info_divs:
            tt = info_div.find('div',{'class':'tt'})
            con = info_div.find('div',{'class':'con'})
            _now_keyword = None
            if tt ==None:
                print(info_div)
                exit()
            for keyword in self.key_words:
                if keyword in tt.get_text().strip():
                    _now_keyword = keyword
            
            ps = con.find_all('p')
            for p in ps:
                p_content = p.get_text()
                
                if p_content == "":
                    continue
                #---------------开特例--------------
                if name == "李梦瑶" and not isinstance(p, NavigableString):#
                    spans = p.find_all('span')
                    if len(spans)>12:
                        _keyword = None
                        break
                #-----------------------------------------
                if len(p_content)<16:
                    for _keyword in self.key_words:
                        if _keyword in p_content:
                            _now_keyword = _keyword
                            continue
                elif not _now_keyword == None:
                    if self.data[self.translation[_now_keyword]] == "None":
                        self.data[self.translation[_now_keyword]] = p_content
                    elif _now_keyword != "研究方向":
                        self.data[self.translation[_now_keyword]] += "<br/>" + p_content

        self.get_brief()
        self.down_load()
        return self.Brief_version
    
    def institution_11(self):
        totle_div = self.soup.find('div', id ='zoom')
        if not totle_div:
            return ["Error"]

        try:
            info_tables = totle_div.find_all('table', attrs={'cellspacing': '1', 'cellpadding': '0', 'width': '100%', 'align': 'center', 'bgcolor': '#CCCCCC'})
            #------------------小信息在info_table[0]里--------------------------
            
            # print(info_tables,self.url)
            # exit()
            small_info = info_tables[0]
            small_trs = small_info.find_all('tr')
            img = small_info.find('img')
            if img:
                self.data["img"] = "https://waiyuan.njfu.edu.cn" + img['src']
            for small_tr in small_trs:
                tds = small_tr.find_all('td')
                now_keyword = None
                for td in tds:
                    content = td.get_text().strip()
                    if now_keyword == None:
                        for key_word in self.key_words:
                            if key_word in content:
                                now_keyword = key_word
                                break
                    else:
                        self.data[self.translation[now_keyword]] = content
                        now_keyword = None
            #------------------大信息在info_table[1]里--------------------------
            
            more_info = info_tables[1]
            more_trs = more_info.find_all('tr')
            for more_tr in more_trs:
                _tds = more_tr.find_all('td')
                _now_keyword = None
                for _td in _tds:
                    _content = _td.get_text().strip()
                    if _now_keyword == None:
                        for _key_word in self.key_words:
                            if _key_word in _content:
                                _now_keyword = _key_word
                                break
                    else:
                        if self.data[self.translation[_now_keyword]] == "None":
                            self.data[self.translation[_now_keyword]] = ""
                        self.data[self.translation[_now_keyword]] += _content + "<br/>"
                        _now_keyword = None

            self.get_brief()
            self.down_load()
            return self.Brief_version
        except Exception:
            return ["Error"]
    
    def institution_12(self):#网页打开没内容
        first_tag = self.soup.find('span', attrs={'style': 'font-size:14px'})
        self.data["Name"] = first_tag.get_text()
        self.get_brief()
        self.down_load()
        return self.Brief_version
    
    def institution_13(self):
        total_info = self.soup.find('table', attrs={'width': '100%', 'height': '48', 'border': '0', 'cellpadding': '0', 'cellspacing': '0', 'id': 'showjs'})
        if not total_info:
            return ["Error"]
        #-----------姓名-----------
        name_span = total_info.find('span')
        self.data["Name"] = name_span.text
        #-----------小信息------------
        small_table = total_info.find('table', attrs={'cellspacing': '1', 'cellpadding': '0', 'width': '100%', 'align': 'center', 'border': '0'})
        img = small_table.find('img')
        if img:
            if self.College_id == "13":
                self.data["img"] = "https://jiaju.njfu.edu.cn" + img['src']
            elif self.College_id == "14":
                self.data["img"] = "https://qg.njfu.edu.cn" + img['src']

        p_tags = small_table.find_all('p')
        for p in p_tags:
            p_content = p.text
            content_head = p_content
            if len(content_head)>16:
                content_head = content_head[:16]

            for keyword in self.key_words:
                if keyword in content_head:
                    self.data[self.translation[keyword]] = p_content[2:]#把前3个字符剃掉，因为多余了
        #-----------大信息------------
        more_table = total_info.find('table', attrs={'cellspacing': '0', 'cellpadding': '0', 'width': '100%', 'align': 'center', 'border': '0'})
        trs = more_table.find_all('tr')

        now_keyword = None
        for tr in trs:
            if now_keyword == None:
                content = tr.get_text().strip()
                for key_word in self.key_words:
                    if key_word in content:
                        now_keyword = key_word
                        break
            else:
                ps = tr.find_all('p')
                for p in ps[1:]:
                    p_text = p.get_text().strip()
                    if p_text == "":
                        continue

                    if self.data[self.translation[now_keyword]] == "None":
                        self.data[self.translation[now_keyword]] = p_text
                    else:
                        self.data[self.translation[now_keyword]] += "<br/>" + p_text
                now_keyword = None

        #----------------------------
        self.get_brief()
        self.down_load()
        return self.Brief_version
    
    def institution_14(self):#别看他短小，但是是完成了的！
        return self.institution_13()
    
    def institution_15(self):#汽车工程学院
        self.key_words.remove("姓名")#应为姓名是单独放的，所以这个学院要把“姓名”关键词移除
        #----------------获得小信息-------------------
        small_info = self.soup.find('table', attrs={'width': '100%', 'border': '0', 'cellspacing': '0', 'cellpadding': '10'})
        imgs = self.soup.find_all('img')
        if len(imgs)>1 and imgs[2]['src'] != "":
            picture = "https://jty.njfu.edu.cn" + imgs[2]['src']
            self.data["img"] = picture

        small_trs = small_info.find_all('tr')
        name_tr = small_trs[0]
        name_span = name_tr.find_all('span')[0]
        self.data["Name"] = name_span.text

        for small_tr in small_trs[1:]:
            small_spans = small_tr.find_all('span')
            for small_span in small_spans:
                content = small_span.text.strip()

                # if "研究方向" in content:#针对40作优化
                #     continue

                for key_word in self.key_words:
                    if key_word in content and content!= "":
                        if self.data[self.translation[key_word]] == "None":
                            self.data[self.translation[key_word]] = content
                        else:
                            self.data[self.translation[key_word]] +=content
                        #--------------------因为个别老师的文本而开的特例--------------------------
                        if key_word == "研究方向":
                            self.key_words.remove("研究方向")
                            self.key_words.remove("研究领域")
                        #-----------------------------------------------------------------------
                        break
        self.key_words.remove("电话")
        self.key_words.remove("邮箱")
        self.key_words.remove("Office Address")
        self.key_words.remove("E-Mail")

        #----------------获得大信息-------------------
        more_info = self.soup.find('table', attrs={'cellspacing': '1', 'cellpadding': '0', 'width': '100%', 'align': 'center', 'border': '0'})
        trs = more_info.find_all('tr')
        contents = []
        for tr in trs:
            ps = tr.find_all('p')
            #-------------开特例------------------
            if self.person_id == "0040":
                ps = ps[1:]
            #-------------开特例------------------
            if len(ps)>0:
                for p in ps[2:]:
                    p__content = p.get_text().strip().replace('\xa0',"")

                    if p__content != "" and not p__content in contents:
                        contents.append(p__content)
            else:#这是没p标签，得到的是次级标题的头
                spans = tr.find_all('span')
                for span in spans:
                    span_content = span.get_text().strip().replace('\xa0',"")

                    if span_content != "":
                        contents.append(span_content)


        unique_list = []
        for item in contents:
            if item not in unique_list:
                unique_list.append(item.replace('\t',''))
        #-------------开特例------------------
        # if self.person_id == "0040":
        #     unique_list = unique_list[1:]
        #-----------------------------------------

        now_keyword = None
        for elem in unique_list:
            elem_head = elem
            if len(elem_head)>16:#每个元素都进行一次头关键词检索，并更新当前关键词
                elem_head = elem_head[:16]#只取前16个用作头判断
            for keyword in self.key_words:
                if keyword in elem_head:
                    now_keyword = keyword
                    break
            

            if now_keyword != None:#字符串长度大于16时才判断为不只是标题
                if self.data[self.translation[now_keyword]] == "None" or now_keyword == "联系方式":
                    self.data[self.translation[now_keyword]] = ""
                self.data[self.translation[now_keyword]] += elem + "<br/>"



        self.get_brief()
        self.down_load()
        return self.Brief_version
    
    def institution_16(self):
        # total_info = self.soup.find('table',id='showjs')
        # #----------------小信息----------------
        # name = total_info.find('span', style="font-size:16px;line-height:25px").text
        # self.data["Name"] = name
        # small_info = total_info.find('table', cellspacing="1", cellpadding="0", width="100%", align="center", border="0")
        # img = small_info.find('img')
        # if img['src']:
        #     self.data["img"] = "https://cee.njfu.edu.cn/" + img['src']

        # small_ps = small_info.find_all('p')[1:]
        # for small_p in small_ps:
        #     p_text = small_p.get_text().strip()
        #     for key_word in self.key_words:
        #         if key_word in p_text:
        #             p_text = p_text[3:]
        #             if self.data[self.translation[key_word]] == "None":
        #                 self.data[self.translation[key_word]] = p_text
        #             else:
        #                 self.data[self.translation[key_word]] += "   " + p_text
        # #----------------大信息----------------
        # more_info = total_info.find('table', {'cellspacing': '0', 'cellpadding': '0', 'width': '100%', 'align': 'center', 'border': '0'})
        # trs = more_info.find_all('tr')
        # contents = []

        # #self.key_words.insert(0,name)
        # #self.translation[name] = "Introduction"

        # result = [more_info.get_text().strip().replace('\xa0',"").replace('\u202c',"")]  # 初始化结果列表，将原始字符串作为第一个元素
        # for keyword in self.key_words:
        #     temp = []  # 临时列表用于存放拆分后的结果
        #     for item in result:
        #         splitted = item.split(keyword)  # 根据关键词拆分字符串
        #         temp.extend(splitted)  # 将拆分后的结果添加到临时列表中
        #     result = temp  # 更新结果列表为拆分后的临时列表


        # print(result)
        # exit()


        # for tr in trs:#把文本处理成列表形式，方便读取
        #     #td = .find('td')
        #     ps = tr.find_all('p')
        #     #print(len(ps))
        #     for p in ps:
        #         p__content = p.get_text().strip().replace('\xa0',"").replace('\n',"")
        #         if "经历" in p__content:
        #             break
        #         elif p__content != "":
        #             contents.append(p__content)
        # contents = contents[1:]
        # for cont in contents:
        #      print(cont+"\n-----------------------------------------")
        # exit()

        # self.get_brief()
        # self.down_load()
        # return self.Brief_version
        return ["Error"]


    def institution_17(self):
        return ["Error"]
        # self.get_brief()
        # self.down_load()
        # return self.Brief_version
    
    def institution_18(self):
        total_info = self.soup.find('div', {'class': 'container-body'})
        name_div = total_info.find('div', {'class': 'name'})
        name = name_div.find_all('span')[0].text
        self.data["Name"] = name

        img = total_info.find('img')
        if img:
            self.data["img"] = "https://sky.njfu.edu.cn/" + img['src']
        #------------------基本信息------------------
        intro_div = total_info.find('div',{'class':'intro'})
        intro_ps =intro_div.find_all('p')
        for intro_p in intro_ps:
            intro_p_content = intro_p.text.strip()
            for key_word in self.key_words:
                if key_word in intro_p_content and intro_p_content[3:] != "":
                    if self.data[self.translation[key_word]] == "None":
                        self.data[self.translation[key_word]] = intro_p_content[3:]
                    else:
                        self.data[self.translation[key_word]] += intro_p_content[3:]
        #------------------brief信息-----------------
        brief_info = total_info.find('div',{'class':'brief'})
        brief_ps = brief_info.find_all('p')
        if brief_ps:#有的他没有这个里面的p标签
            self.data["Introduction"] = brief_ps[0].text.strip()
            brief_keyword = None
            for brief_p in brief_ps:
                brief_p_content = brief_p.text.strip()
                content_head = brief_p_content
                if len(content_head)>16:
                    content_head = content_head[:16]

                skip = False
                for keyword in self.key_words:
                    if keyword in content_head:
                        brief_keyword = keyword
                        skip = True
                        break
                
                if brief_keyword != None and skip == False and brief_p_content != "":
                    if self.data[self.translation[brief_keyword]] == "None":
                        self.data[self.translation[brief_keyword]] = brief_p_content
                    else:
                        self.data[self.translation[brief_keyword]] += "   " + brief_p_content
        #--------------achieve信息-----------------
        achieve_divs = total_info.find_all('div',{'class':'achieve'})
        if achieve_divs:
            for achieve_div in achieve_divs:
                title_div = achieve_div.find('div',{'class':'title'})
                title = title_div.get_text().strip()
                works_div = achieve_div.find('div',{'class':'works'})
                works = works_div.get_text().strip()

                for _keyword in self.key_words:
                    if _keyword in title:
                        ps = works_div.find_all('p')
                        for p in ps:
                            p_content = p.get_text()
                            if p_content == "":
                                continue
                            if self.data[self.translation[_keyword]] == "None":
                                self.data[self.translation[_keyword]] = ""
                            self.data[self.translation[_keyword]] += p_content + "<br/>"


        self.get_brief()
        self.down_load()
        return self.Brief_version
    