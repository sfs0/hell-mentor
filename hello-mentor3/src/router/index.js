import {
  createRouter,
  createWebHistory
} from "vue-router";


const routes = [{
    path: "/",
    name: "home",
    component: () => import("@/views/Home2.vue"),
  },
  {
    // path: "/first",
    path: "/concise/:id",
    name: "first",
    component: () => import("@/views/First.vue"),
  },
  {
    path: "/detail/:conciseId/:id",
    name: "second",
    component: () => import("@/views/Second3.vue"),
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  // 在进入或离开特殊页面时，添加或移除 body 样式
  if (to.name === 'home') {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = 'auto';
  }

  next();
});

export default router;