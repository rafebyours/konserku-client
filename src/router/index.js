import { createRouter, createWebHistory } from "vue-router";
import IndexPage from "@/pages/index.vue"
import LoginPage from "@/pages/auth/login.vue"
import RegisterPage from "@/pages/auth/register.vue"
const routes = [
    {
        path: "/",
        name: "Home",
        component: IndexPage
    },
    {
        path: "/login",
        name: "Login",
        component: LoginPage
    },
    {
        path: "/register",
        name: "Register",
        component: RegisterPage
    }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { left: 0, top: 0 };
  },
});


export default router;