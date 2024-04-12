<template>
  <div class="book">
    <NavBar msg="Welcome to Your Vue.js App" />
    <!-- <h1>Book Dashboard</h1> -->
  </div>
  <div></div>
  <div class="col-lg-10 offset-lg-1">
    <!-- Heading -->
    <h3 class="mb-3 mt-4">History</h3>
    <!-- Divider -->
    <hr class="my-7" />

    <!-- List group -->
    <ul
      class="list-group list-group-lg list-group-flush-y list-group-flush-x mb-7"
    >
      <li
        class="list-group-item my-2 rounded border"
        v-for="book in reversedBooks"
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
              Issue Date: {{ book.date_issue }} <br />
              Return Date: {{ book.return_date }} <br />
            </div>
          </div>
          <div class="col-4">
            <!-- Image -->
            <a
              :class="{
                'btn btn-success mb-1': book.status === 'Returned',
                'btn btn-warning mb-1': book.status === 'Overdue',
                'btn btn-danger mb-1': book.status === 'Rejected',
                'btn btn-info mb-1': book.status === 'Revoked',
              }"
              :href="book_path(book.book_id)"
              :style="{ maxWidth: '210px', minWidth: '150px' }"
            >
              {{ book.status }}
            </a>
            <br />
            <button
              class="btn btn-info mt-1"
              style="max-width: 210px; min-width: 150px"
              hidden
            >
              Edit Request
            </button>
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
  name: "HistoryView",
  components: {
    NavBar,
  },
  data() {
    return {
      books: [],
    };
  },
  beforeCreate() {
    const token = localStorage.getItem("library_management_system_token");
    this.$store.commit("setNav", "History");
    fetch(API_URL + "/history", {
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
        if (data.history.length === 0) {
          this.button_message = "No Books to Return";
        }
        console.log(data.history.length);
        this.$store.commit("setUser", data.history[0].username);
        this.$store.commit("setNav", "History");
        this.books = data.history;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  },
  methods: {
    fetchbookimg(bookId) {
      return API_URL + "/fetchbookimg/" + bookId;
    },
    book_path(bookId) {
      return "/book/" + bookId;
    },
  },
  computed: {
    reversedBooks() {
      // Return a reversed copy of the books array
      return this.books.slice().reverse();
    },
  },
};
</script>
