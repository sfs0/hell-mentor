<template>
    <div class="nav-container">
        <div class="nav2" @click="handleClick">
            <img src="/images/logo1.png" height="80" />
        </div>
        <div class="nav1" @click="handleClick">
            <img src="/images/xiaoxun.png" alt="校训" />
        </div>
    </div>
</template>
<script>
export default {
    name: 'Nav',
    methods: {
        handleClick() {
            // 在这里执行自定义操作，然后进行路由导航
            this.$router.push({ name: 'home' });
        },
    },
};
</script>
<style scoped>
.nav-container {
    display: flex;
    justify-content: space-between;
    padding: 20px 260px 20px 50px;
    /* 调整上下左右的间距 */
    opacity: 0.9;
}

.nav1,
.nav2 {
    width: 200px;
}
</style>
