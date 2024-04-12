<template>
  <div class="book">
    <NavBar msg="Welcome to Your Vue.js App" />
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
        v-for="book in books.requested_books"
        v-bind:key="book[0].book_id"
      >
        <div class="row align-items-center">
          <div class="col-4">
            <!-- Image -->
            <a :href="book_path(book[0].book_id)">
              <img
                :src="fetchbookimg(book[0].book_id)"
                alt="..."
                class="img-fluid"
                style="width: 110px; height: 140px; border-radius: 0.5rem"
              />
            </a>
          </div>
          <div class="col">
            <!-- Title -->
            <p class="mb-4 fs-sm fw-bold">
              <a class="text-body" :href="book_path(book[0].book_id)"
                >{{ book[1].book_name }}: {{ book[1].title }}</a
              >
              <br />
              <!-- <span class="text-muted">$40.00</span> -->
            </p>

            <!-- Text -->
            <div class="fs-sm text-muted">
              Author: {{ book[1].author }} <br />
              Issue Date: {{ book[0].date_issue }} <br />
              Return Date: {{ book[0].return_date }} <br />
            </div>
          </div>
          <div class="col-4">
            <!-- Image -->
            <button
              class="btn btn-warning mb-1"
              style="max-width: 210px; min-width: 150px"
              v-on:click="return_book(book[0].book_id)"
            >
              Return</button
            ><br />
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
    <!-- Button -->
    <button class="btn w-100 btn-dark" v-on:click="return_all_books()">
      {{ button_message }}
    </button>
  </div>
</template>
<script>
import NavBar from "@/components/NavBar.vue";
import { API_URL } from "../../constants";
export default {
  name: "RequestedBooksView",
  components: {
    NavBar,
  },
  data() {
    return {
      books: [],
      currentDate: "",
      returnDate: "-----",
      refreshIntervalId: "",
      status: "Request for Book",
      button_message: "Return All Books",
    };
  },
  beforeCreate() {
    const token = localStorage.getItem("library_management_system_token");
    this.$store.commit("setNav", "My Books");
    fetch(API_URL + "/requested_books/" + "Issued", {
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
        console.log(data);
        if (data.requested_books.length === 0) {
          this.button_message = "No Books to Return";
        }
        this.$store.commit("setUser", data.current_user.username);
        this.$store.commit("setNav", "My Books");
        this.books = data;
        try {
          this.book_id_selected = this.books.requested_books[0][0].book_id;
        } catch (error) {
          console.log();
        }
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
    return_book(id) {
      try {
        let data = {
          book_id: id,
        };
        const token = localStorage.getItem("library_management_system_token");
        fetch(API_URL + "/return_book", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-access-token": token,
          },
          body: JSON.stringify(data),
        })
          .then((response) => {
            if (response.status == 401) {
              this.$router.push("/unauthorized");
            } else {
              return response.json();
            }
          })
          .then((data) => {
            if (data.status !== "success") {
              alert(data.message);
            } else {
              alert(data.message);
              window.location.reload();
            }
          })
          .catch((error) => {
            console.error("Error fetching data4:", error);
          });
      } catch (error) {
        console.error("Error fetching data5:", error);
      }
    },
    return_all_books() {
      try {
        const token = localStorage.getItem("library_management_system_token");
        fetch(API_URL + "/return_all_books", {
          method: "POST",
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
            if (data.status !== "success") {
              alert(data.message);
            } else {
              alert(data.message);
              window.location.reload();
            }
          })
          .catch((error) => {
            console.error("Error fetching data6:", error);
          });
      } catch (error) {
        console.error("Error fetching data7:", error);
      }
    },
  },
};
</script>
