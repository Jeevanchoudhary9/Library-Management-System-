<template>
  <div class="book">
    <NavBar msg="Welcome to Your Vue.js App" />
    <!-- <h1>Book Dashboard</h1> -->
  </div>
  <div class="container-fluid text-center" style="margin-top: 2%">
    <div class="row">
      <div class="col-md-3 order-md-first" style="margin-bottom: 10px">
        <div class="mx-2">
          <img
            :src="fetchbookimg(this.$route.params.id)"
            class="card-img-top mx-2"
            style="width: 100%; height: 500px"
            alt="..."
          />
        </div>
      </div>
      <div class="col-md-6">
        <div class="card mx-2" style="width: 100%">
          <div class="card-body">
            <p
              class="fs-3 fw-semibold text-justify-center my-0"
              style="text-align: left"
            >
              {{ current_book.book_name }}: {{ current_book.title }}
            </p>
            <p
              class="text-justify-center"
              style="text-align: left; color: gray"
            >
              By: {{ current_book.author }}
            </p>
            <hr />
            <p
              class="fw-medium text-justify-center my-0"
              style="
                text-align: left;
                color: black;
                font-size: 15px;
                white-space: pre-line;
              "
            >
              {{ current_book.description }}
            </p>
            <a
              href="#"
              class="btn fw-medium d align-items-center justify-content-center"
              style="
                background-color: rgb(254, 210, 19);
                border-radius: 20px;
                margin-top: 20px;
              "
              >Add To Wishlist</a
            >
          </div>
        </div>
      </div>
      <div class="col-md-3 order-md-last">
        <!-- last col -->
        <div class="card mx-2" style="width: 100%">
          <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <p class="card-text">
              3 Some quick example text to build on the card title and make up
              the bulk of the card's content.
            </p>
            <!-- <a
              :href="'/request_book/' + 1"
              class="btn fw-medium d align-items-center justify-content-center"
              style="background-color: rgb(253, 147, 24); border-radius: 20px"
              >Request for Book</a
            > -->
            <button
              type="button"
              :hidden="status !== 'Request for Book'"
              class="btn fw-medium d align-items-center justify-content-center"
              style="background-color: rgb(253, 147, 24); border-radius: 20px"
              data-bs-toggle="modal"
              data-bs-target="#myModal"
            >
              {{ status }}
            </button>
            <button
              type="button"
              :hidden="status !== 'Cancel Request'"
              class="btn fw-medium d align-items-center justify-content-center"
              style="background-color: gray; border-radius: 20px; color: white"
              v-on:click="cancel_request()"
            >
              {{ status }}
            </button>
            <div class="modal" id="myModal">
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
                              <a href="">
                                <img
                                  :src="fetchbookimg(this.$route.params.id)"
                                  class="mx-2"
                                  style="width: 90px; height: 110px"
                                  alt="..."
                                />
                              </a>
                            </div>
                            <div class="col">
                              <!-- Title -->
                              <p class="fs-sm fw-bold">
                                <a class="text-body" href="product.html"
                                  >{{ current_book.book_name }}:
                                  {{ current_book.title }} ({{
                                    current_book.status
                                  }})</a
                                >
                              </p>

                              <!-- Text -->
                              <div class="fs-sm text-muted">
                                Author: {{ current_book.author }}<br />
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
                              <span class="ms-auto fs-sm" id="date">{{
                                currentDate
                              }}</span>
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
                                id="timeperiod"
                                required
                              />
                              <select
                                class="form-control form-control-sm"
                                id="unitselection"
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
                              <span class="ms-auto fs-sm" id="datereturn">{{
                                returnDate
                              }}</span>
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
                        v-on:click="request()"
                      >
                        Request for Book
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="container mx-4">
      <hr style="width: 93%" />
      <p
        class="fw-semibold text-justify-center my-0"
        style="text-align: left; color: black; font-size: 20px"
      >
        Recommandation
      </p>
    </div>
    <div class="row">
      <div class="col-12" style="margin-top: 20px">
        <div
          class="mx-2"
          style="height: 384px; overflow-x: auto; margin-right: 200px"
        >
          <ol class="list-unstyled d-flex">
            <li
              class="mx-4"
              v-for="books in data.books"
              :key="books.book_id"
              style="width: 202px"
            >
              <a
                class=""
                :href="'/book/' + books.book_id"
                style="text-decoration: none"
              >
                <img
                  alt="{{ books.book_name }}: {{ books.title }}"
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

  <!-- <div class="container-fluid">
    <div class="row">
      <div class="card mx-2" style="width: 18rem">
        <img :src="fetchbookimg(2)" class="card-img-top my-2" alt="..." />
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
          <p class="card-text">
            Some quick example text to build on the card title and make up the
            bulk of the card's content.
          </p>
          <a href="#" class="btn btn-primary">Go somewhere</a>
        </div>
      </div>
      <div class="card mx-2" style="width: 18rem">
        <img :src="fetchbookimg(3)" class="card-img-top my-2" alt="..." />
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
          <p class="card-text">
            Some quick example text to build on the card title and make up the
            bulk of the card's content.
          </p>
          <a href="#" class="btn btn-primary">Go somewhere</a>
        </div>
      </div>
      <div class="card mx-2" style="width: 18rem">
        <img :src="fetchbookimg(4)" class="card-img-top my-2" alt="..." />
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
          <p class="card-text">
            Some quick example text to build on the card title and make up the
            bulk of the card's content.
          </p>
          <a href="#" class="btn btn-primary">Go somewhere</a>
        </div>
      </div>
    </div>
  </div> -->
  <!-- <div>
    <div>right <img :src="fetchbookimg(1)" alt="Image" /></div>
  </div>
  {{ data }} -->
</template>
<script>
import NavBar from "@/components/NavBar.vue";
import { API_URL } from "../../constants";
export default {
  name: "BookView",
  data() {
    return {
      data: [],
      current_book: [],
      currentDate: "",
      returnDate: "-----",
      refreshIntervalId: "",
      status: "Request for Book",
    };
  },
  beforeCreate() {
    const token = localStorage.getItem("library_management_system_token");
    this.$store.commit("setNav", "books");
    fetch(API_URL + "/book/" + this.$route.params.id, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        this.$store.commit("setUser", data.user_data.username);
        if (data.status !== "success") {
          localStorage.removeItem("library_management_system_token");
          this.$router.push("/signin");
        } else {
          this.$store.commit("setUser", data.user_data.username);
          this.$store.commit("setNav", "books");
          this.data = data;
          this.current_book = data.current_book;
          if (data.issue == "Requested") {
            this.status = "Cancel Request";
          }
        }
        console.log(data);
        console.log(this.current_book);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        this.$router.push("/signin");
      });
  },
  components: {
    NavBar,
  },
  methods: {
    fetchbookimg(bookId) {
      return API_URL + "/fetchbookimg/" + bookId;
    },
    date() {
      return new Date().toLocaleString();
    },
    updateDate() {
      let date = new Date().getTime();
      this.currentDate = new Date(date).toLocaleString();
    },
    updatereturnDate() {
      try {
        let date = new Date().getTime();
        let period = document.getElementById("timeperiod").value;
        let selection = document.getElementById("unitselection").value;
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
        console.error("Error fetching data:", error);
      }
    },
    request() {
      try {
        let period = document.getElementById("timeperiod").value;
        let selection = document.getElementById("unitselection").value;
        console.log(period, selection);
        let data = {
          book_id: this.$route.params.id,
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
              console.log("1");
              console.log(data);
            } else {
              alert(data.message);
              console.log("2");
              console.log(data);
              window.location.reload();
            }
          })
          .catch((error) => {
            console.error("Error fetching data:", error);
          });
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    cancel_request() {
      try {
        let data = {
          book_id: this.$route.params.id,
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
              console.log("1");
              console.log(data);
            } else {
              alert(data.message);
              console.log("2");
              console.log(data);
              window.location.reload();
            }
          })
          .catch((error) => {
            console.error("Error fetching data:", error);
          });
      } catch (error) {
        console.error("Error fetching data:", error);
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
  mounted() {
    try {
      this.updateDate();
      this.updatereturnDate();
      setInterval(this.updateDate, 1000);
      this.refreshIntervalId = setInterval(this.updatereturnDate, 1000);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  },
  beforeUnmount() {
    try {
      clearInterval(this.refreshIntervalId);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  },
};
</script>
<style></style>
