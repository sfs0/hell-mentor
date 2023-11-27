<template>
    <div class="main">
        <div style="background-color: rgb(52, 110, 80); height: 462px; padding-top: 8px;" @click="handleClick">
            <Nav />
        </div>

        <div class="common-layout-container">
            <div class="common-layout1">
                <el-header class="header-flex">
                    <div class="header-content1">
                        <!-- 图片部分 -->
                        <el-image style="width: 168px; height: 230px;  margin:20px 75px 0px 75px;" :src="jsonData.img"
                            :fit="cover">
                            <template #error>
                                <div class="image-slot">
                                    <el-icon size="100">
                                        <Picture />
                                    </el-icon>
                                </div>
                            </template>
                        </el-image>
                        <!-- 图片下方的姓名部分 -->

                    </div>
                    <!-- 保持其他部分不变，只修改 header-content2 的样式 -->
                    <div class="header-content2">
                        <!-- 文字部分 -->
                        <div class="name-container">
                            <div class="name1">{{ jsonData.Name }}</div>
                            <!-- 如果有简介信息，则显示 -->

                            <div class="name2">
                                {{ keyTranslations['Research_direction'] }}:
                                <span v-if="jsonData.Research_direction
                                    !== '' && jsonData.Research_direction !== 'None'"
                                    v-html="renderHtml(jsonData.Research_direction)">
                                </span>
                                <span v-else>
                                    导师暂未填写信息
                                </span>
                            </div>
                            <div class="name2">
                                {{ keyTranslations['Final_Degree'] }}:
                                <span v-if="jsonData.Final_Degree
                                    !== '' && jsonData.Final_Degree !== 'None'"
                                    v-html="renderHtml(jsonData.Final_Degree)">
                                </span>
                                <span v-else>
                                    导师暂未填写信息
                                </span>
                            </div>


                            <div class="name2">
                                {{ keyTranslations['Contact_information'] }}:
                                <span v-if="jsonData.Contact_information
                                    !== '' && jsonData.Contact_information !== 'None'"
                                    v-html="renderHtml(jsonData.Contact_information)">
                                </span>
                                <span v-else>
                                    导师暂未填写信息
                                </span>
                            </div>
                        </div>
                    </div>
                </el-header>
            </div>


            <div class="other"></div>


            <div class="common-layout2">
                <el-container>
                    <el-main>
                        <div v-if="loading" class="loading">数据加载中...</div>
                        <el-row :gutter="20" v-else>
                            <el-col :span="24">
                                <el-collapse v-model="activeCollapse">
                                    <el-collapse-item v-for="(key, index) in orderedKeys" :key="key" :name="index"
                                        class="manualBook">
                                        <template #title>
                                            <div class="custom-title">
                                                <!-- 这里添加自定义的标题样式 -->
                                                {{ keyTranslations[key] }}:
                                            </div>
                                        </template>
                                        <div v-if="key !== 'img' && key !== 'Name'" :class="{
                                            'info-content': true,
                                            'highlighted': highlightedRow === index,
                                        }">
                                            <div v-if="jsonData[key] === 'None' || jsonData[key] === ''" class="info-value">
                                                导师还没有在这里留下足迹哦~
                                            </div>
                                            <div v-else class="info-value" v-html="renderHtml(jsonData[key])"></div>

                                        </div>
                                    </el-collapse-item>
                                </el-collapse>
                            </el-col>
                        </el-row>
                        <div class="pagination-buttons">
                            <router-link v-if="currentPage > 1"
                                :to="{ name: 'second', params: { conciseId, id: (currentPage - 1).toString().padStart(4, '0') } }"
                                class="pagination-button">
                                上一页
                            </router-link>
                            <span class="current-page">
                                当前页: {{ currentPage }} / {{ totalPages }}
                            </span>
                            <router-link v-if="currentPage < totalPages"
                                :to="{ name: 'second', params: { conciseId, id: (currentPage + 1).toString().padStart(4, '0') } }"
                                class="pagination-button">
                                下一页
                            </router-link>
                        </div>
                        <div v-if="currentPage === 1" class="page-message">已经是第一页</div>
                        <div v-if="currentPage === totalPages" class="page-message">已经是最后一页</div>
                    </el-main>
                </el-container>
            </div>

            <div class="footer">

            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import Nav from '@/components/Nav2.vue';
import DOMPurify from 'dompurify';

export default {
    components: {
        Nav,
    },
    data() {
        return {
            jsonData: {},
            id: this.$route.params.id,
            conciseId: this.$route.params.conciseId,
            orderedKeys: [
                "Department",
                "Duties",
                "Category",
                "Final_Education",
                "Paper",
                "Patent",
                "Achievements",
                "Class",
                "Topic",
                "Projects",
                "Services_Activities",
                "Award_status",
                "Introduction",
                "Biographical_notes",
                "Work",
                "Homepage",
                "Title",
                "Professional_affiliations",
                "Experience"
            ],
            keyTranslations: {
                "Department": "所属系",
                "Duties": "职务",
                "Category": "类别",
                "Final_Education": "最终学历",
                'Final_Degree': '最终学位',
                'Research_direction': '研究方向',
                'Contact_information': '联系方式',
                "img": "照片",
                "Paper": "论文",
                "Patent": "专利",
                "Achievements": "成果",
                "Class": "课程",
                "Topic": "课题",
                "Projects": "项目",
                "Services_Activities": "服务与学术活动",
                "Award_status": "荣誉和获奖",
                "Introduction": "简介",
                "Biographical_notes": "简历",
                "Work": "著作",
                "Homepage": "主页",
                "Title": "职称",
                "Professional_affiliations": "社会兼职",
                "Experience": "经历"
            },
            highlightedRow: null,
            totalPages: 0,
            currentPage: Number(this.$route.params.id),

            loading: true,
            activeCollapse: [], // 控制展开的 el-collapse-item 的数组
            activeCollapse: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        };
    },
    mounted() {
        this.loadData();

    },
    watch: {
        $route(to, from) {
            this.id = to.params.id;
            window.scrollTo(0, 0);
            // 监听路由变化，重新加载数据
            this.loadData();
        },
    },
    methods: {
        loadData() {
            this.loading = true;
            this.currentPage = Number(this.$route.params.id);
            // 显示信息
            axios.get(`/news/${this.conciseId}/${this.id}.json`)
                .then(res => {
                    this.jsonData = res.data;
                })
                .catch(err => {
                    console.error('Error fetching JSON file:', err);
                })
                .finally(() => {
                    this.loading = false;
                });

            // 计算总数
            axios.get(`/university/${this.conciseId}.json`)
                .then(res => {
                    this.totalPages = Math.ceil(Object.keys(res.data).length);
                })
                .catch(err => {
                    console.error(err);
                });
        },
        highlightRow(index) {
            this.highlightedRow = index;
        },
        resetHighlight() {
            this.highlightedRow = null;
        },
        renderHtml(htmlString) {
            return DOMPurify.sanitize(htmlString);
        },
    },
};
</script>

<style scoped>
.main {
    position: relative;
    background-color: rgb(245, 245, 245);
    width: 100%;
    min-height: 100vh;
    overflow: auto;
}

.footer {
    margin-top: 30px;
    background-color: rgb(52, 110, 80);
    height: 30px;
}

.common-layout-container {
    position: absolute;
    top: 130px;
    /* 调整这个值以控制 common-layout 的位置 */
    width: 100%;

}

.common-layout1 {
    background-color: #fff;
    margin: 10px auto;
    width: 69.3%;
    height: 100%;
    padding: 10px;
    box-sizing: border-box;


}

.common-layout2 {

    background-color: #fff;
    margin: 10px auto;
    width: 69.3%;

    padding: 10px;
    box-sizing: border-box;
}

.el-header {
    height: auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 10px;
    padding: 10px;
    border-radius: 10px;
    width: 100%;

}

.header-content2 {
    width: 110vh;
    margin: 0 0 0 0px;
    padding: 0;
}


.profile-image {
    width: 100px;
    height: 100px;
    border-radius: 50%;
}

/* 在样式中添加以下规则，确保文字靠左 */
.name-container {
    display: flex;
    flex-direction: column;
    padding-right: 75px;
}

.name1 {
    font-size: 45px;
    font-weight: bold;
    font-family: "SmileySans-Oblique";
    color: rgb(52, 110, 80);
    margin-bottom: 10px;
    margin-top: 30px;
}

.name2 {
    font-family: "SmileySans-Oblique";
    font-size: 24px;
    margin-bottom: 20px;
    text-align: left;
    color: rgb(80, 80, 80);
}

.el-main {
    height: auto;
    background-color: #fff;
    margin: 10px 0;
    border-radius: 10px;
    opacity: 0.9;

}



.info-content {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    border-radius: 5px;
}

.info-content:hover {
    background-color: rgb(248, 248, 248);

    border-style: dashed;
    border: 1px;
}

.other {
    margin-top: 0px;
    padding-top: 0px;
    margin-bottom: 30px;
    background-color: black;
}

.info-value {
    margin-left: 30px;
    font-size: 18px;

    color: rgb(60, 60, 60);
}



.pagination-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}

.pagination-button {
    cursor: pointer;
    color: rgb(52, 110, 80);
    text-decoration: underline;
}

.current-page {
    font-weight: bold;
}

.loading {
    text-align: center;
    padding: 20px;
    font-weight: bold;
    color: rgb(52, 110, 80);
}

.page-message {
    text-align: center;
    padding: 5px;
    font-weight: bold;
    color: rgb(52, 110, 80);
}

.custom-title {
    color: rgb(52, 110, 80);
    padding: 10px;

    font-size: 24px;
    font-family: "SmileySans-Oblique";
}

:deep(.el-collapse-item__header) {
    background-color: #fff;
    height: 60px;
}

:deep(.el-collapse-item__wrap) {

    background-color: #fff;
    height: auto;
}

.el-collapse-item {
    border-bottom: 1px solid rgb(248, 248, 248);
}
</style>
