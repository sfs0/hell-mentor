import {
    createApp
} from "vue";
import App from "./App.vue";
import router from "./router";

import 'bootstrap/dist/css/bootstrap.min.css'; // 导入 Bootstrap 样式
import 'bootstrap/dist/js/bootstrap.min'; // 导入 Bootstrap


import ElementPlus from 'element-plus' // 引入Element Plus 所需
import 'element-plus/dist/index.css' // 引入Element Plus 所需

import * as ElementPlusIconsVue from '@element-plus/icons-vue' // 引入Element Plus icon 所需
import '@/assets/font/font.css';


const app = createApp(App);

// 引入Element Plus icon 所需
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component);
}

app.use(router);
app.use(ElementPlus); // 引入Element Plus 所需
app.mount('#app');