import json
import os
import get_category
import get_teachers_link
import core_code
import attributes


class Information_Institute:
    College_website = {
        1: "https://linxue.njfu.edu.cn/",
        2: "https://wood.njfu.edu.cn/",
        3: "https://hg.njfu.edu.cn/szdw/xkdtr/",
        4: "https://jidian.njfu.edu.cn/szdw/index.html",
        5: "https://tumu.njfu.edu.cn/",
        6: "https://cem.njfu.edu.cn/szdw.asp",
        7: "7.txt",
        8: "https://it.njfu.edu.cn/",
        9: "https://yuanlin.njfu.edu.cn/",
        10: "10.txt",
        11: "https://waiyuan.njfu.edu.cn//szdw/szml/index.html",
        12: "https://art.njfu.edu.cn/szdw/jsfc/",
        13: "https://jiaju.njfu.edu.cn/xjdw/index.html",
        14: "https://qg.njfu.edu.cn/szdw/index.html",
        15: "https://jty.njfu.edu.cn/szdw/index.html",
        16: "https://cee.njfu.edu.cn/szdw/zzjs/",
        17: "https://szw.njfu.edu.cn/class_type.asp?id=496/",
        18: "https://sky.njfu.edu.cn/szdw/index.html",
    }

    def __init__(self, College_id: int):
        self.source_path = attributes.get_download_position()
        self.Brief_infos = []
        self.College_id: int = College_id  # 应上级部门的要求，信息院为8
        self.category_urls = get_category.get_category(
            self.College_id, self.College_website[self.College_id]
        )  # 获取目录链接

        # print(self.category_urls)
        # print(len(self.urls))
        # exit()

        self.teacher_urls = []
        # 改成单独一个for虽然降低了性能，但是方便测试维护
        for category_url in self.category_urls:  # 每个目录链接的老师链接都获取
            ready_append = get_teachers_link.teacher_links(
                self.College_id, category_url
            )
            self.teacher_urls.extend(ready_append)

        # print(self.urls)
        # print(len(temp_links))
        # print(temp_links)
        # exit()

        person_id = 1  # 应上级部门的要求，从0开始改为从1开始，是每个人的编号，暂时不互通
        if self.teacher_urls == []:
            print("编号为" + str(self.College_id) + "的学院每个老师的链接获取失败！")
            exit()

        if not os.path.exists(self.source_path):  # 还是得判断一次是否存在目录，就算没有文件也要创建个空目录
            os.makedirs(self.source_path)

        for link in self.teacher_urls:
            person = core_code.main_code(
                link,
                "{:04}".format(person_id),
                self.source_path,
                self.College_website[self.College_id],
                str(self.College_id),
            )  # 将返回的简要信息放进对应的id里
            brief_ = person.tackle()
            if brief_ == ["Error"]:  # 判断是否出现没有内容的页面
                continue

            self.Brief_infos.append(brief_)
            del person
            person_id += 1

        brief_path = self.source_path + "university/"  # 这里改简要信息目录文件夹名
        if not os.path.exists(brief_path):  # 写出信息院的师资简要信息
            os.makedirs(brief_path)
        with open(
            brief_path + str(self.College_id) + ".json", "w", encoding="utf-8"
        ) as file:
            json.dump(self.Brief_infos, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    for i in range(1, 19):
        if i != 16 and i != 17:
            print("学院" + str(i) + "正在获取数据...")
            tea = Information_Institute(i)

    print("任务结束！")
