<template>
    <div style="background-color: rgb(52, 110, 80); height: 140px; padding-top: 8px;">
        <Nav />
    </div>
    <div class="page-container">
        <el-container class="layout-container-demo" style="height:750px;  width: 600px; ">
            <!-- 侧边栏 -->

            <el-aside width=" 360px">
                <!-- 收缩/展开按钮 -->
                <div style="display: flex;    justify-content: center; padding-top: 25px;">
                    <el-radio-group v-model="isCollapse" style="margin-bottom: 20px;" fill="rgb(52, 110, 80)">
                        <el-radio-button :label="false" @click="Collapse('expand')"><span
                                style="font-size: 20px; padding: 26px;">展
                                开</span></el-radio-button>
                        <el-radio-button :label="true" @click="Collapse('collapse')"><span
                                style="font-size: 20px; padding: 26px;">收
                                起</span></el-radio-button>
                    </el-radio-group>
                </div>
                <!-- 菜单项 -->
                <el-menu default-active="1" class="el-menu-vertical-demo" :collapse="isCollapse">
                    <template v-for="(value, key) in items" :key="key">
                        <el-menu-item :index="key" @click="getInformation(key)">
                            <el-icon>
                                <document />
                            </el-icon>
                            <template #title><span style="font-size: large;">{{ value }}</span></template>
                        </el-menu-item>
                    </template>
                </el-menu>
            </el-aside>


            <!-- 主体内容 -->
            <el-container>

                <el-main>

                    <!-- 滚动条容器 -->
                    <el-scrollbar ref="tableScrollbar">
                        <!-- 搜索框 -->
                        <div class="search-container">
                            <el-icon class="search-icon">
                                <Search />
                            </el-icon>
                            <el-input v-model="searchKeyword" placeholder="请输入关键词进行搜索" clearable
                                style="height: 50px;"></el-input>
                        </div>
                        <!-- 表格 -->
                        <el-table :data="filteredTableData" height="1600" :header-row-style="{
                            color: 'rgb(52, 110, 80)', fontSize: '24px',
                        }" :header-cell-style="{
    height: '60px',
}" ref="dataTable" border>
                            <!-- 图片列 -->
                            <el-table-column label="照片" width="140">
                                <template #default="{ row }">
                                    <el-image style="width: 111px; height: 148px; border-radius: 10px;" :src="row.img"
                                        :fit="cover" @click="goToSecond(row.id)">
                                        <template #error>
                                            <div style="text-align: center;">
                                                <el-icon size="100">
                                                    <Picture />
                                                </el-icon>
                                                <span>暂无导师照片</span>
                                            </div>

                                        </template>
                                    </el-image>
                                </template>
                            </el-table-column>
                            <!-- 姓名列 -->
                            <el-table-column prop="Name" label="姓名" width="120">
                                <template #default="{ row }">
                                    <!-- 使用 highlight 方法进行关键词高亮 -->
                                    <div v-html="highlight(row.Name)" style="font-size: large;"></div>
                                </template>
                            </el-table-column>
                            <!-- 研究方向列 -->
                            <el-table-column prop="Research_direction" label="研究方向" max-width="750px">
                                <template #default="{ row }">
                                    <div v-if="row.Research_direction !== 'None' && row.Research_direction !== ''">
                                        <!-- 使用 highlight 方法进行关键词高亮 -->
                                        <div v-html="highlight(row.Research_direction)" style="font-size: large;"></div>
                                    </div>
                                    <div v-else style="font-size: large;">请导航到详细信息查看</div>
                                </template>
                            </el-table-column>
                            <!-- 查看详细信息按钮列 -->
                            <el-table-column label="详细信息" width="200">
                                <template #default="{ row }">
                                    <el-button type="text" @click="goToSecond(row.id)"
                                        style="color: rgb(52, 110, 80); font-size: 20px;">
                                        详情<el-icon>
                                            <Right />
                                        </el-icon>
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-scrollbar>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script>

import axios from 'axios';
import Nav from '@/components/Nav.vue';

export default {
    components: {
        Nav,
    },
    name: 'concise',

    data() {
        return {
            items: null,
            isCollapse: false,
            collegeId: '1',
            tableData: [],
            searchKeyword: '', // 存储搜索关键词
            currentRowKey: null,
        };
    },
    computed: {
        // 根据搜索关键词过滤表格数据
        filteredTableData() {
            console.log('this.tableData:', this.tableData);
            if (Array.isArray(this.tableData)) {
                return this.tableData.filter(item => {
                    return (
                        (item.Name.includes(this.searchKeyword) ||
                            item.Research_direction.includes(this.searchKeyword)) && (
                            item.Name !== '' &&
                            item.Name !== null)
                    );
                });
            } else {
                console.error('this.tableData is not an array');
                return [];
            }
        },
    },
    methods: {
        // 跳转到第二页
        goToSecond(id) {
            var conciseId = this.collegeId;
            this.$router.push({ name: 'second', params: { id, conciseId }, });
        },
        // 处理侧边栏的收缩/展开
        Collapse(type) {
            this.isCollapse = type === 'collapse';
        },
        // 获取信息
        getInformation(id) {
            this.collegeId = id;
            this.$router.push({ name: 'first', params: { id } });
            var temp = '/university/' + id + '.json';
            axios.get(temp).then(res => {
                this.tableData = res.data;

                // 数据加载后滚动到表格顶部
                this.$nextTick(() => {
                    const tableScrollbar = this.$refs.tableScrollbar;
                    if (tableScrollbar) {
                        tableScrollbar.scrollTo(0, 0);
                    }
                });
            }).catch(err => {
                console.log(err);
            });
        },
        // 将匹配关键词的部分用 <span> 标签高亮显示
        highlight(text) {
            if (!this.searchKeyword) {
                return text;
            }
            const pattern = new RegExp(`(${this.searchKeyword})`, 'gi');
            return text.replace(pattern, '<span style="background-color: yellow; color: rgb(82, 159, 78); font-weight: bold;">$1</span>');
        },


    },
    mounted() {
        axios.get(`/news/college.json`).then(res => {
            this.items = res.data;
        }).catch(err => {
            console.log(err);
        });
        this.getInformation(this.collegeId);

    },

};
</script>

<style scoped>
.main {
    background-image: url('/public/images/background.png');
    background-size: cover;
    width: 100%;
    min-height: 100vh;
    overflow: auto;
}

.page-container {
    display: flex;
    justify-content: center;
    margin: 20px 100px 0px 100px;
}

.el-aside {

    background-color: #fff;
    opacity: 0.9;
    border-radius: 10px;
}

.el-main {

    background-color: #fff;
    opacity: 0.9;
    border-radius: 0px 10px 10px 0px;
}

.el-menu {
    border-radius: 10px;
}

.el-scrollbar {
    border-radius: 10px;
}


.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: auto;
    min-height: 400px;
}

.el-menu-vertical-demo:not(.el-menu--collapse) .el-menu-item.is-active {
    background-color: rgb(229, 231, 230);
    /* 选中时的背景颜色 */
    color: rgb(52, 110, 80);
    /* 选中时的文字颜色 */
}

.el-menu-vertical-demo:not(.el-menu--collapse) .el-menu-item:hover {
    background-color: rgb(52, 110, 80);
    color: #fff;
}

.el-header {
    height: 250px;
    background-size: cover;
}

.search-container {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    /* 调整垂直间距，根据需要调整 */
}

.search-icon {
    font-size: 30px;
    margin-right: 10px;
    /* 调整图标与输入框之间的水平间距，根据需要调整 */
}
</style>
