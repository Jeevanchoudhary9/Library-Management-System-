<template>
  <div class="home vh-100 bg-image">
    <NavBar msg="Welcome to Library Management System" />
    <h1>User Dashboard</h1>
    {{ bookimg }}
    <!-- <li v-for="section in data.books_lst_section" :key="section.id">
      <li v-for="books in section">{{ books }}--------------------</li>
    </li> -->
    <img :src="imageSrc1" alt="Image" />
    <img :src="imageSrc2" alt="Image" />
    <img :src="imageSrc3" alt="Image" />
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
                  <!-- <img
                    alt="Never Lie: An addictive psychological thriller"
                    :src="getBookImageUrl(books.book_id)"
                    style="max-width: 177px; max-height: 266px"
                   /> -->
                  <img :src="'imageSrc' + 1" alt="Image" />

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
import NavBar from "@/components/NavBar.vue";
import { API_URL } from "../../constants";
import axios from "axios";

export default {
  name: "UserDashboardView",
  components: {
    NavBar,
  },
  data() {
    return {
      data: [],
      bookimg: {},
    };
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
          console.log(data.books[0].book_id);
          this.data = data;

          // Iterate over each book and fetch its image
          this.data.books.forEach((book) => {
            this.getBookImageUrl(book.book_id);
          });
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  },
  methods: {
    getBookImageUrl(bookId) {
      // Check if image source already fetched, if not fetch it
      axios
        .get(API_URL + "/fetchbookimg/" + bookId, {
          responseType: "blob",
        })
        .then((response) => {
          const reader = new FileReader();
          reader.onload = () => {
            // Ensure that imageSrc1 and bookimg are properly defined in the data object
            this.imageSrc1 = reader.result;
            this.bookimg[bookId] = reader.result; // Assuming you want to store it as an object
            console.log(this.bookimg);
          };
          reader.readAsDataURL(response.data); // Read the blob data as data URL
        })
        .catch((error) => {
          console.error("Error fetching image:", error);
        });
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
