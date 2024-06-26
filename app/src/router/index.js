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
    path: "/bookread/:id",
    name: "bookread",
    component: () => import("../views/BookRead.vue"),
  },
  {
    path: "/bookreadadmin/:id/",
    name: "bookreadadmin",
    component: () => import("../views/AdminBookRead.vue"),
  },
  {
    path: "/adminbook/:id",
    name: "adminbook",
    component: () => import("../views/AdminBookView.vue"),
  },
  {
    path: "/search/:search",
    name: "search",
    component: () => import("../views/SearchView.vue"),
    beforeEnter: (to, from, next) => {
      if (to.params.search === "") {
        next({ name: "userdashboard" }); // Redirect to dashboard route
      } else {
        next(); // Continue navigation
      }
    },
  },
  {
    path: "/request/:id",
    name: "request_book",
    component: () => import("../views/RequestedBooksView.vue"),
  },
  {
    path: "/requested_books/Requested",
    name: "requested_books",
    component: () => import("../views/RequestedBooksView.vue"),
  },
  {
    path: "/requested_books/Issued",
    name: "issued_books",
    component: () => import("../views/MyBooksView.vue"),
  },
  {
    path: "/history",
    name: "history",
    component: () => import("../views/HistoryView.vue"),
  },
  {
    path: "/admin_dashboard",
    name: "admin_dashboard",
    component: () => import("../views/AdminDashboardView.vue"),
  },
  {
    path: "/unauthorized",
    name: "unauthorized",
    component: () => import("../views/UnauthorizedView.vue"),
  },
  {
    path: "/adminbookissue",
    name: "adminbookissue",
    component: () => import("../views/AdminBookIssueView.vue"),
  },
  {
    path: "/issuedbooks",
    name: "issuedbooks",
    component: () => import("../views/IssuedBooksView.vue"),
  },
  {
    path: "/adminsummary",
    name: "adminsummary",
    component: () => import("../views/AdminSummaryView.vue"),
  },
  {
    path: "/usersummary",
    name: "usersummary",
    component: () => import("../views/UserSummaryView.vue"),
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
