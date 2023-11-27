<template>
    <div class="nav-container">
        <div class="nav2">
            <img src="/images/logo1.png" height="80" />
        </div>
        <div class="nav1">
            <div @click="backConcise" style="font-size: 50px; color: #fff; font-family: SmileySans-Oblique;">返回列表</div>
        </div>
    </div>
</template>
<script>
export default {
    methods: {
        backConcise() {
            this.$router.push('/concise/1');
        },
    },
};


</script>


<style scoped>
.nav-container {
    display: flex;
    justify-content: space-between;
    padding: 20px 0px 20px 50px;
    /* 调整上下左右的间距 */
    opacity: 0.9;
}

.nav1 {
    width: 250px;
}

.nav2 {
    width: 200px;
}
</style>
