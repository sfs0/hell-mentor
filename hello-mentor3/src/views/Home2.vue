<template>
    <div class="background">
        <!-- 添加Logo -->
        <img src="/images/njfulogo.png" alt="Logo" class="logo" />

        <!-- 使用 transition 包裹动态文字 -->
        <transition name="fade" @after-enter="animationEnd">
            <div ref="content" v-if="showGreeting" class="content" :style="animatedStyle">
                <div class="text-container">
                    <div style="font-weight: bold; font-size: 100px;">{{ greeting }}</div>

                    <div class="char">{{ greeting2 }}</div>
                </div>
                <br />
                <!-- 添加按钮 -->
                <el-button type="primary" round class="my-button" @click="redirectToPage" :style="buttonStyle"
                    @mouseenter="buttonHover(true)" @mouseleave="buttonHover(false)">
                    我要寻师
                    <el-icon>
                        <Right />
                    </el-icon>
                </el-button>
            </div>
        </transition>

    </div>
</template>

<script>
export default {
    data() {
        return {
            showGreeting: false, // 控制文字显示
            greeting: '导师, 您好', // 显示的文字
            greeting2: 'Hello, Mentor',
            buttonStyle: {}, // 按钮样式
        };
    },
    methods: {
        redirectToPage() {
            this.$router.push('/concise/1');
        },
        animationEnd() {
            // 动画结束后将 showGreeting 设置为 true，并将 left 的值设回原始值
            this.showGreeting = true;
            this.$refs.content.style.left = '25%';
        },
        buttonHover(isHover) {
            // 根据鼠标悬停状态设置按钮样式
            this.buttonStyle = isHover ? { background: 'rgb(52, 110, 80)', border: '3px solid white', height: '130px', width: '433px' } : {};
        },
    },
    computed: {
        animatedStyle() {
            // 根据 showGreeting 的值设置动画样式
            return this.showGreeting ? {} : { animation: 'slideInFromLeft 1s ease-out' };
        },

    },
    mounted() {
        // 在组件加载后一定时间后显示文字
        setTimeout(() => {
            // 触发从左浮现的动画
            this.showGreeting = true;
        }, 1000); // 1000毫秒后显示，你可以根据需要调整时间
        // 隐藏主要内容区域

    },

};
</script>
<style scoped>
.background {
    background-image: url('/public/images/background.png');
    background-size: cover;
    height: 100vh;
    width: 100vw;

    position: relative;
}

.logo {
    position: absolute;
    width: 1800px;
    height: auto;
}


.my-button {
    width: 400px;
    height: 120px;
    font-size: 60px;
    background: transparent;
    border: 3px solid white;
    border-radius: 20px;
    color: white;
    padding: 10px;
    margin-top: 30px;
}

.content {
    font-family: Georgia, 'Times New Roman', Times, serif;
    position: absolute;
    top: 50%;
    left: -50%;
    /* 将 left 的值设为负的一半宽度，使整体容器从页面最左侧开始移动 */
    transform: translate(-50%, -50%);
    font-size: 80px;
    color: #fff;
    white-space: nowrap;
    overflow: hidden;
}

.text-container {
    display: inline-block;
    opacity: 0;
    animation: fadeIn 0.5s ease forwards, slideInFromLeft 1s ease-out;
}

/* 调整 keyframes 以包含移动和透明度 */
@keyframes fadeIn {
    to {
        opacity: 1;
    }
}

@keyframes slideInFromLeft {
    from {
        transform: translateX(-100%);
        opacity: 0;
    }

    to {
        transform: translateX(0);
        opacity: 1;
    }
}
</style>
