<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand d-flex align-items-center" href="/">
        <img
          src="@/assets/img/logo.jpeg"
          alt=""
          width="35"
          height="35"
          class="d-inline-block align-text-top mx-4"
        />
        Library Management System
        <code
          class="mx-2 ps-md-2 border-start border-md border-gray text-danger"
        >
          {{ username }}'s {{ nav }}
        </code>
      </a>
      <div class="d-flex">
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto px-8 mb-2 mb-lg-0">
            <li class="nav-item mx-2">
              <a class="nav-link active" aria-current="page" href="/">Home</a>
            </li>
            <li
              class="nav-item mx-2 ps-md-4 border-start border-md border-gray"
            >
              <a class="nav-link" href="/requested_books/Requested"
                >Requested Books</a
              >
            </li>
            <li
              class="nav-item mx-2 ps-md-4 border-start border-md border-gray"
            >
              <a class="nav-link" href="/requested_books/Issued">My Books</a>
            </li>
            <li
              class="nav-item mx-2 ps-md-4 border-start border-md border-gray"
            >
              <a class="nav-link" href="/history">History</a>
            </li>
            <li
              class="nav-item mx-2 ps-md-4 border-start border-md border-gray"
            >
              <a class="nav-link" href="/usersummary">Summary</a>
            </li>
            <li
              class="nav-item mx-2 ps-md-4 border-start border-md border-gray"
            >
              <a class="nav-link" href="/logout">Logout</a>
            </li>
          </ul>
          <!-- <button @click="click">send data</button> -->
        </div>
      </div>
    </div>
  </nav>
</template>
<script>
import "bootstrap";
import { mapState } from "vuex";
export default {
  name: "NavBar",
  data() {
    return {
      username: "default",
      navid: "1",
    };
  },
  methods: {
    // click() {
    //   console.log(this.userData);
    // },
  },
  computed: {
    ...mapState(["userData", "navData"]),
  },
  created() {
    this.username = this.userData;
    this.nav = this.navData;
  },
};
</script>
<style>
@import "~bootstrap/dist/css/bootstrap.min.css";
</style>
