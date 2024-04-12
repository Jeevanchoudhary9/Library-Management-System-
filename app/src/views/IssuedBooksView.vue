<template>
  <div class="book">
    <NavBar_admin msg="Welcome to Your Vue.js App" />
    <!-- <h1>Book Dashboard</h1> -->
  </div>
  <div></div>
  <div class="col-lg-10 offset-lg-1">
    <!-- Heading -->
    <h3 class="mb-3 mt-4">Issued Books</h3>
    <!-- Divider -->
    <hr class="my-7" />

    <!-- List group -->
    <ul
      class="list-group list-group-lg list-group-flush-y list-group-flush-x mb-7"
    >
      <li
        class="list-group-item my-2 rounded border"
        v-for="book in books"
        v-bind:key="book[0].book_id"
      >
        <div class="row align-items-center">
          <div class="col-4">
            <!-- Image -->
            <a href="">
              <img
                :src="fetchbookimg(book[0].book_id)"
                alt="..."
                class="img-fluid"
                style="width: 150px; height: 190px; border-radius: 0.5rem"
              />
            </a>
          </div>
          <div class="col">
            <!-- Title -->
            <p class="mb-4 fs-sm fw-bold">
              <a class="text-body" href=""
                >{{ book[1].book_name }}: {{ book[1].title }}</a
              >
              <br />
              <!-- <span class="text-muted">$40.00</span> -->
            </p>

            <!-- Text -->
            <div class="row">
              <div class="col">
                <div class="fs-sm text-muted">
                  <b>Username:</b> {{ book[2].username }} <br />
                  <b>Name:</b> {{ book[4].firstname }} {{ book[4].lastname
                  }}<br />
                  <b>Email:</b> {{ book[4].email }} <br />
                  <b>Phone:</b> {{ book[4].phone }} <br />
                </div>
              </div>
              <div class="col">
                <div class="fs-sm text-muted">
                  <b>Author:</b> {{ book[1].author }} <br />
                  <b>Section:</b> {{ book[3].section_name }} <br />
                  <b>Issue Date:</b> {{ book[0].date_issue }} <br />
                  <b>Return Date:</b> {{ book[0].return_date }} <br />
                </div>
              </div>
            </div>
          </div>
          <div class="col-4">
            <!-- Image -->
            <button
              class="btn btn-danger mb-1"
              v-on:click="revoke(book[0].book_id)"
              :style="{ maxWidth: '210px', minWidth: '150px' }"
            >
              Revoke Access
            </button>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>
<script>
import NavBar_admin from "@/components/NavBar_admin.vue";
import { API_URL } from "../../constants";
export default {
  name: "IssuedBooksView",
  components: {
    NavBar_admin,
  },
  data() {
    return {
      books: [],
    };
  },
  beforeCreate() {
    const token = localStorage.getItem("library_management_system_token");
    this.$store.commit("setNav", "Issued Books");
    fetch(API_URL + "/adminbookissued", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": token,
      },
    })
      .then((response) => {
        if (response.status == 401) {
          this.$router.push("/unauthorized");
        } else {
          console.log("2");
          return response.json();
        }
      })
      .then((data) => {
        console.log(data);
        this.$store.commit("setUser", data.current_user.username);
        this.$store.commit("setNav", "Issued Books");
        this.books = data.issues;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  },
  methods: {
    fetchbookimg(bookId) {
      return API_URL + "/fetchbookimg/" + bookId;
    },
    revoke(bookId) {
      const token = localStorage.getItem("library_management_system_token");
      fetch(API_URL + "/revokeaccess/" + bookId, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": token,
        },
      })
        .then((response) => {
          if (response.status == 401) {
            this.$router.push("/unauthorized");
          } else {
            return response.json();
          }
        })
        .then((data) => {
          alert(data.message);
          window.location.reload();
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
  },
  computed: {
    // reversedBooks() {
    //   // Return a reversed copy of the books array
    //   return this.books.slice().reverse();
    // },
  },
};
</script>
