def get_keywords():
    key_words = [
        "姓名",
        "研究方向",
        "研究领域",
        "论文",
        "发表文章",
        "专利",
        "成果",
        "课程",
        "课题",
        "项目",
        "服务与学术活动",
        "获奖",
        "荣誉",
        "联系方式",
        "系别",
        "系科部门",
        "职务",
        "职称",
        "类别",
        "最终学历",
        "最终学位",
        "电话",
        "邮箱",
        "著作",
        "简介",
        "简况",
        "简历",
        "个人情况",
        "E-Mail",
        "Office Address",
        "主页",
        "社会兼职",
        "经历",
    ]  # 为保证土木院，不能加“电话”、“邮件”
    return key_words


def get_translation():
    translation = {
        "姓名": "Name",
        "研究方向": "Research_direction",
        "研究领域": "Research_direction",
        "论文": "Paper",
        "发表文章": "Paper",
        "专利": "Patent",
        "成果": "Achievements",
        "课程": "Class",
        "课题": "Topic",
        "项目": "Projects",
        "服务与学术活动": "Services_Activities",
        "荣誉": "Award_status",
        "获奖": "Award_status",
        # "教师编号":"id",
        # "照片":"img",
        "系别": "Department",
        "系科部门": "Department",
        "职务": "Duties",
        "职称": "Title",
        "类别": "Category",
        "最终学历": "Final_Education",
        "最终学位": "Final_Degree",
        "联系方式": "Contact_information",
        "电话": "Contact_information",
        "邮箱": "Contact_information",
        "Office Address": "Contact_information",
        "E-Mail": "Contact_information",
        "著作": "Work",
        "简介": "Introduction",
        "简况": "Introduction",
        "个人情况": "Introduction",
        "简历": "Biographical_notes",
        "主页": "Homepage",
        "社会兼职": "Professional_affiliations",
        "经历": "Experience",
    }
    return translation


def get_initialize_data():
    data = {  # 这个必须定义为实例属性
        "Research_direction": "None",
        "Paper": "None",
        "Patent": "None",
        "Achievements": "None",
        "Class": "None",
        "Topic": "None",
        "Projects": "None",
        "Services_Activities": "None",
        "Award_status": "None",
        "Contact_information": "None",
        "Introduction": "None",
        "id": "None",
        "img": "None",
        "Department": "None",
        "Duties": "None",
        "Title": "None",
        "Category": "None",
        "Final_Education": "None",
        "Final_Degree": "None",
        "Final_Education": "None",
        "Work": "None",
        "Name": "None",
        "Biographical_notes": "None",
        "Homepage": "None",
        "Professional_affiliations": "None",
        "Experience": "None",
    }
    return data


def get_brief_info():
    Brief_version = {
        "id": "None",
        "Name": "None",
        "Research_direction": "None",
        "img": "None",
    }
    return Brief_version


def get_download_position():  # 修改下载目录
    return "D:/"
