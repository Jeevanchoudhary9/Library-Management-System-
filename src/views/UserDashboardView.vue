<template>
  <div class="home vh-100 bg-image">
    <NavBar msg="Welcome to Library Management System" />
    <h1>User Dashboard</h1>

    <!-- <li v-for="section in data.books_lst_section" :key="section.id">
      <li v-for="books in section">{{ books }}--------------------</li>
    </li> -->
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
                  :href="'/signin' + books.book_id"
                  style="text-decoration: none"
                >
                  <img
                    alt="Never Lie: An addictive psychological thriller"
                    src="https://m.media-amazon.com/images/I/41oCesFWhdL._PJku-sticker-v7,TopRight,0,-50._SY315_.jpg"
                    style="max-width: 177px; max-height: 266px"
                  />
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

                <span
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
                >
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import NavBar from "@/components/NavBar.vue";
import { API_URL } from "../../constants";
export default {
  name: "UserDashboardView",
  components: {
    NavBar,
  },
  beforeCreate() {
    const token = localStorage.getItem("library_management_system_token");
    fetch(API_URL + "/dashboard", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status != "success") {
          localStorage.removeItem("library_management_system_token");
          this.$router.push("/signin");
        } else {
          this.$store.commit("setUser", data.user_data.username);
          this.$store.commit("setNav", "dashboard");
          console.log(data);
          this.data = data;
        }
      });
  },
  data() {
    return {
      data: [],
    };
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
