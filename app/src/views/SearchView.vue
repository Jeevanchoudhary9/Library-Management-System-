<template>
  <div class="home vh-100 bg-image">
    <NavBar msg="Welcome to Library Management System" />
    <div class="input-group"></div>
    <h3 style="margin-top: 20px">Welcome to World of Books!</h3>
    <div
      class="row justify-content-center"
      style="margin-right: 20px; margin-left: 20px; margin-bottom: 20px"
    >
      <div class="col-10">
        <input
          type="search"
          class="form-control rounded"
          placeholder="Search"
          aria-label="Search"
          aria-describedby="search-addon"
          v-model="searchText"
        />
      </div>
      <div class="col-1">
        <a
          :href="'/search/' + searchText"
          class="btn btn-outline-primary w-100"
        >
          Search
        </a>
      </div>
    </div>

    <!-- <li v-for="section in data.books_lst_section" :key="section.id">
        <li v-for="books in section">{{ books }}--------------------</li>
      </li> -->
    <!-- <img :src="fetchbookimg(1)" alt="Image" /> -->
    <ul
      class="list-group list-group-lg list-group-flush-y list-group-flush-x mb-7"
      style="margin-right: 100px; margin-left: 100px"
    >
      <li
        class="list-group-item my-2 rounded border"
        v-for="book in data"
        v-bind:key="book.book_id"
      >
        <div class="row align-items-center">
          <div class="col-4">
            <!-- Image -->
            <a :href="book_path(book.book_id)">
              <img
                :src="fetchbookimg(book.book_id)"
                alt="..."
                class="img-fluid"
                style="width: 110px; height: 140px; border-radius: 0.5rem"
              />
            </a>
          </div>
          <div class="col">
            <!-- Title -->
            <p class="mb-4 fs-sm fw-bold">
              <a class="text-body" :href="book_path(book.book_id)"
                >{{ book.book_name }}: {{ book.title }}</a
              >
              <br />
              <!-- <span class="text-muted">$40.00</span> -->
            </p>

            <!-- Text -->
            <div class="fs-sm text-muted">
              Author: {{ book.author }} <br />
              Section: {{ book.section_name }} <br />
            </div>
          </div>
          <div class="col-4">
            <!-- Image -->
            <a
              class="btn btn-info mb-1"
              :href="book_path(book.book_id)"
              :style="{ maxWidth: '210px', minWidth: '150px' }"
            >
              Move to Book
            </a>
            <br />
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import { API_URL } from "../../constants";

export default {
  name: "UserDashboardView",
  components: {
    NavBar,
  },
  data() {
    return {
      data: [],
      searchText: "",
    };
  },
  onload() {
    window.location.reload();
  },
  beforeCreate() {
    const token = localStorage.getItem("library_management_system_token");
    this.$store.commit("setNav", "dashboard");
    if (this.$route.params.search === "") {
      // Redirect to dashboard route
      this.$router.push("/");
    } else {
      fetch(API_URL + "/search/" + this.$route.params.search, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": token,
        },
      })
        .then((response) => {
          if (response.status == 401) {
            console.log("1");
            this.$router.push("/unauthorized");
          } else {
            console.log("2");
            return response.json();
          }
        })
        .then((data) => {
          console.log(data);
          if (data.status != "success") {
            console.log("1");
            //   localStorage.removeItem("library_management_system_token");
            //   this.$router.push("/signin");
          } else {
            console.log("2");
            this.$store.commit("setUser", data.user_data.username);
            console.log(data);
            this.data = data.books;
          }
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }
  },
  methods: {
    fetchbookimg(bookId) {
      return API_URL + "/fetchbookimg/" + bookId;
    },
    book_path(bookId) {
      return "/book/" + bookId;
    },
  },
};
</script>
<style>
@import "~bootstrap/dist/css/bootstrap.min.css";
.hover-red:hover {
  color: red !important;
}
/* body {
    background-image: url('@/assets/img/wood.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: repeat-y;
  } */
</style>
