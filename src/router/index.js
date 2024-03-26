import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "userdashboard",
    component: () => import("../views/UserDashboardView.vue"),
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import("../views/SignupView.vue"),
  },
  {
    path: "/signin",
    name: "signin",
    component: () => import("../views/SigninView.vue"),
  },
  {
    path: "/addbook",
    name: "addbook",
    component: () => import("../views/AddbooksView.vue"),
  },
  {
    path: "/book/:id",
    name: "book",
    component: () => import("../views/BookView.vue"),
  },
  {
    path: "/logout",
    name: "logout",
    component: () => import("../views/LogoutView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
