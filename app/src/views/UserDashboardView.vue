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
        />
      </div>
      <div class="col-1">
        <button
          v-on:click="search()"
          type="button"
          class="btn btn-outline-primary w-100"
          data-mdb-ripple-init
        >
          Search
        </button>
      </div>
    </div>

    <!-- <li v-for="section in data.books_lst_section" :key="section.id">
      <li v-for="books in section">{{ books }}--------------------</li>
    </li> -->
    <!-- <img :src="fetchbookimg(1)" alt="Image" /> -->
    <div
      v-for="section in data.books_lst_section"
      :key="section.id"
      class="container-fluid px-0"
      style="width: 95%"
    >
      <div class="row">
        <div class="col-12 d-flex align-items-start">
          <h3
            class="a-size-large a-spacing-small mr-auto mb-0"
            style="font-weight: bold"
          >
            {{ section[0].section_name }}
          </h3>
        </div>
        <div class="col-12">
          <hr aria-hidden="true" class="a-spacing-base a-divider-normal mt-1" />
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <div
            class="mx-2"
            style="height: 384px; overflow-x: auto; margin-right: 200px"
          >
            <ol class="list-unstyled d-flex">
              <li
                class="mx-4"
                v-for="books in section"
                :key="books.book_id"
                style="width: 202px"
              >
                <a
                  class=""
                  :href="'/book/' + books.book_id"
                  style="text-decoration: none"
                >
                  <img
                    alt="Never Lie: An addictive psychological thriller"
                    :src="fetchbookimg(books.book_id)"
                    style="
                      max-width: 177px;
                      max-height: 266px;
                      min-height: 177px;
                      min-height: 266px;
                    "
                  />
                  <!-- <img :src="'imageSrc' + 1" alt="Image" /> -->

                  <br />
                  <div
                    style="
                      font-size: small;
                      font-weight: bold;
                      color: darkblue;
                      width: 200px;
                    "
                    class="hover-red"
                  >
                    {{ books.book_name }}: {{ books.title }}
                  </div>
                </a>

                <!-- <span
                  style="
                    font-size: small;
                    font-weight: bold;
                    color: grey;
                    text-decoration: none;
                  "
                  >Kindle Price:</span
                >
                <span
                  style="
                    font-size: medium;
                    font-weight: lighter;
                    color: red;
                    text-decoration: none;
                  "
                  >$3.99</span
                > -->
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>
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
    };
  },
  beforeCreate() {
    const token = localStorage.getItem("library_management_system_token");
    this.$store.commit("setNav", "dashboard");
    fetch(API_URL + "/dashboard", {
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
          localStorage.removeItem("library_management_system_token");
          this.$router.push("/signin");
        } else {
          console.log("2");
          this.$store.commit("setUser", data.user_data.username);
          console.log(data);
          this.data = data;
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  },
  methods: {
    fetchbookimg(bookId) {
      return API_URL + "/fetchbookimg/" + bookId;
    },
    search() {
      const searchText = document.querySelector('input[type="search"]').value;
      this.$router.push("/search/" + searchText);
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
