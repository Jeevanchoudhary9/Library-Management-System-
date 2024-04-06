<template>
  <div class="book">
    <NavBar msg="Welcome to Your Vue.js App" />
    <!-- <h1>Book Dashboard</h1> -->
  </div>
  <div></div>
  <div class="col-lg-10 offset-lg-1">
    <!-- Heading -->
    <h3 class="mb-3 mt-4">Requested Books</h3>
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
              class="btn btn-danger mb-1"
              style="max-width: 210px; min-width: 150px"
              v-on:click="cancel_request(book[0].book_id)"
            >
              Cancel Request</button
            ><br />
            <button
              class="btn btn-info mt-1"
              style="max-width: 210px; min-width: 150px"
              data-bs-toggle="modal"
              :data-bs-target="'#myModal' + book[0].book_id"
              v-on:click="book_id_selected = book[0].book_id"
            >
              Edit Request
            </button>
            <div class="modal" :id="'myModal' + book[0].book_id">
              <div class="modal-dialog">
                <div class="modal-content">
                  <!-- Modal Header -->
                  <div class="modal-header">
                    <h4 class="modal-title">Request for Book</h4>
                    <button
                      type="button"
                      class="btn-close"
                      data-bs-dismiss="modal"
                    ></button>
                  </div>

                  <!-- Modal body -->
                  <div class="modal-body">
                    <div>
                      <!-- List group -->
                      <ul
                        class="list-group list-group-lg list-group-flush-y list-group-flush-x mb-7"
                      >
                        <li class="list-group-item">
                          <div class="row align-items-center">
                            <div class="col-4">
                              <!-- Image -->
                              <a :href="book_path(book[0].book_id)">
                                <img
                                  :src="fetchbookimg(book[0].book_id)"
                                  class="mx-2"
                                  style="width: 90px; height: 110px"
                                  alt="..."
                                />
                              </a>
                            </div>
                            <div class="col">
                              <!-- Title -->
                              <p class="fs-sm fw-bold">
                                <a
                                  class="text-body"
                                  :href="book_path(book[0].book_id)"
                                >
                                  {{ book[1].book_name }} :
                                  {{ book[1].title }}
                                </a>
                              </p>

                              <!-- Text -->
                              <div class="fs-sm text-muted">
                                Author: {{ book[1].author }} <br />
                                Pages: 1000
                              </div>
                            </div>
                          </div>
                        </li>
                        <hr />
                      </ul>

                      <!-- Card -->
                      <div class="card mb-9 bg-light">
                        <div class="card-body">
                          <ul
                            class="list-group list-group-sm list-group-flush-y list-group-flush-x"
                          >
                            <li class="list-group-item d-flex">
                              <span>Current Date/Time</span>
                              <span class="ms-auto fs-sm" id="date">
                                {{ currentDate }}
                              </span>
                            </li>
                            <li class="list-group-item d-flex">
                              <div
                                class="d-flex justify-content-center align-items-center"
                              >
                                <span>Period of Time</span>
                              </div>
                              <input
                                type="number"
                                class="ms-auto fs-sm mx-2 form-control form-control-sm"
                                style="width: 60px"
                                :id="'timeperiod' + book[0].book_id"
                                required
                              />
                              <select
                                class="form-control form-control-sm"
                                :id="'unitselection' + book[0].book_id"
                                style="width: 60px"
                                required
                              >
                                <option selected value="hrs">hrs</option>
                                <option value="days">days</option>
                                <option value="weeks">weeks</option>
                              </select>
                            </li>
                            <li class="list-group-item d-flex">
                              <span>Return Date/Time</span>
                              <span class="ms-auto fs-sm" id="datereturn">
                                {{ returnDate }}
                              </span>
                            </li>
                            <!-- <li class="list-group-item d-flex fs-lg fw-bold">
                              <span>demo</span>
                              <span class="ms-auto">demo</span>
                            </li> -->
                          </ul>
                        </div>
                      </div>

                      <!-- Disclaimer -->
                      <p class="mb-7 fs-xs text-gray-500 mt-2">
                        After the Return of Date/Time, the book will be
                        automatically returned or the access to user will be
                        revoked.
                      </p>

                      <!-- Button -->
                      <button
                        :disabled="!isDateValid"
                        class="btn w-100 btn-dark"
                        v-on:click="request(book[0].book_id)"
                      >
                        Edit Book Request
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </li>
    </ul>
    <!-- Button -->
    <button class="btn w-100 btn-dark" v-on:click="cancel_all_requests()">
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
      book_id_selected: "",
      button_message: "Cancel All Request",
    };
  },
  mounted() {
    try {
      this.updateDate();
      this.updatereturnDate();
      setInterval(this.updateDate, 1000);
      this.refreshIntervalId = setInterval(this.updatereturnDate, 1000);
    } catch (error) {
      console.error("ss");
    }
  },
  beforeCreate() {
    const token = localStorage.getItem("library_management_system_token");
    this.$store.commit("setNav", "Requested Books");
    fetch(API_URL + "/requested_books/" + "Requested", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data.requested_books.length === 0) {
          this.button_message = "No Requested Books";
        }
        this.$store.commit("setUser", data.current_user.username);
        this.$store.commit("setNav", "Requested Books");
        this.books = data;
        try {
          this.book_id_selected = this.books.requested_books[0][0].book_id;
        } catch (error) {
          console.log();
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        this.$router.push("/signin");
      });
  },
  methods: {
    fetchbookimg(bookId) {
      return API_URL + "/fetchbookimg/" + bookId;
    },
    book_path(bookId) {
      return "/book/" + bookId;
    },
    date() {
      return new Date().toLocaleString();
    },
    updateDate() {
      let date = new Date().getTime();
      this.currentDate = new Date(date).toLocaleString();
    },
    updatereturnDate(book_id = this.book_id_selected) {
      try {
        if (this.books.requested_books.length === 0) {
          return;
        }
        console.log("book_id", book_id);
        let date = new Date().getTime();
        let period = document.getElementById("timeperiod" + book_id).value;
        let selection = document.getElementById(
          "unitselection" + book_id
        ).value;
        if (period === "" || selection === "") {
          this.returnDate = "-----";
          return;
        }
        let time = parseInt(period);
        if (isNaN(time)) {
          this.returnDate = "-----";
          return;
        }
        if (selection === "hrs") {
          time = time * 60 * 60 * 1000;
        } else if (selection === "days") {
          time = time * 24 * 60 * 60 * 1000;
        } else if (selection === "weeks") {
          time = time * 7 * 24 * 60 * 60 * 1000;
        } else {
          time = 0;
        }
        let calculatedDate = new Date(date).getTime() + time;
        this.returnDate = new Date(calculatedDate).toLocaleString();
      } catch (error) {
        // console.error("Error fetching data1:", error);
      }
    },
    request(book_id) {
      try {
        let period = document.getElementById("timeperiod" + book_id).value;
        let selection = document.getElementById(
          "unitselection" + book_id
        ).value;
        let data = {
          book_id: book_id,
          period: period,
          unit: selection,
        };
        const token = localStorage.getItem("library_management_system_token");
        fetch(API_URL + "/request_book", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-access-token": token,
          },
          body: JSON.stringify(data),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status !== "success") {
              alert(data.message);
            } else {
              alert(data.message);
              window.location.reload();
            }
          })
          .catch((error) => {
            console.error("Error fetching data2:", error);
          });
      } catch (error) {
        console.error("Error fetching data3:", error);
      }
    },
    cancel_request(id) {
      try {
        let data = {
          book_id: id,
        };
        const token = localStorage.getItem("library_management_system_token");
        fetch(API_URL + "/cancel_request", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-access-token": token,
          },
          body: JSON.stringify(data),
        })
          .then((response) => response.json())
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
    cancel_all_requests() {
      try {
        const token = localStorage.getItem("library_management_system_token");
        fetch(API_URL + "/cancel_all_requests", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "x-access-token": token,
          },
        })
          .then((response) => response.json())
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
  computed: {
    isDateValid() {
      let period = this.returnDate;
      let time = parseInt(period);
      if (isNaN(time)) {
        return false;
      }
      return true;
    },
  },
  beforeUnmount() {
    try {
      clearInterval(this.refreshIntervalId);
    } catch (error) {
      console.error("Error fetching dasta:", error);
    }
  },
};
</script>
