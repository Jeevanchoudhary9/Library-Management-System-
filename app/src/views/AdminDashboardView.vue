<template>
  <div class="book">
    <NavBar_admin msg="Welcome to Your Vue.js App" />
    <!-- <h1>Book Dashboard</h1> -->
  </div>
  <div class="container mt-5" style="max-width: 90%">
    <div class="border rounded pt-2">
      <div class="mb-2 d-flex justify-content-between align-items-center">
        <div class="mx-5"><strong>Section</strong></div>
        <div class="col-3 text-end mx-5">
          <button
            class="btn btn-primary btn-block"
            data-bs-toggle="modal"
            data-bs-target="#myModal"
            v-on:click="add_section_name()"
          >
            Add Section
          </button>
          <div class="modal" id="myModal">
            <div class="modal-dialog">
              <div class="modal-content">
                <!-- Modal Header -->
                <div class="modal-header">
                  <h4 class="modal-title">{{ title }} Book Section</h4>
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
                    <!-- Card -->
                    <div class="card mb-9 bg-light">
                      <div class="card-body">
                        <ul
                          class="list-group list-group-sm list-group-flush-y list-group-flush-x"
                        >
                          <li class="list-group-item d-flex">
                            <span>Section Name</span>
                            <input
                              type="text"
                              class="ms-auto fs-sm mx-2 form-control form-control-sm"
                              style="width: 120px"
                              id="sectionname"
                              required
                            />
                          </li>
                          <li class="list-group-item d-flex align-items-center">
                            <span>Description</span>
                            <textarea
                              class="ms-auto fs-sm mx-2 form-control form-control-sm"
                              style="width: 120px"
                              id="sectiondescription"
                              required
                            ></textarea>
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
                      Add Section With Description Here
                    </p>

                    <!-- Button -->
                    <button
                      class="btn w-100 btn-dark"
                      :hidden="istitle()"
                      v-on:click="add_section()"
                    >
                      Add Section
                    </button>
                    <button
                      class="btn w-100 btn-dark"
                      :hidden="!istitle()"
                      v-on:click="edit_section()"
                    >
                      Edit Section
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
  <div class="mt-5">
    <div
      v-for="sec in data.section"
      :key="sec.id"
      class="container-fluid px-0"
      style="width: 95%"
    >
      <div class="row">
        <div class="mb-2 d-flex justify-content-between align-items-center">
          <h3
            class="a-size-large a-spacing-small mr-auto mb-0"
            style="font-weight: bold"
          >
            {{ sec[0][0].section_name }}
          </h3>
          <div class="col-3 text-end mx-5">
            <button
              class="btn btn-warning btn-block mx-1"
              data-bs-toggle="modal"
              data-bs-target="#myModal"
              v-on:click="edit_section_name(sec[0][0].section_id)"
            >
              Edit Section
            </button>
            <button
              class="btn btn-primary btn-block mx-1"
              data-bs-toggle="modal"
              data-bs-target="#myModal_addbook"
              v-on:click="edit_section_name(sec[0][0].section_id)"
            >
              Add Books
            </button>
            <button
              class="btn btn-danger btn-block mx-1"
              v-on:click="delete_section(sec[0][0].section_id)"
            >
              Delete Section
            </button>
          </div>
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
                v-for="books in sec[1]"
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
                    {{ books.book_name }} : {{ books.title }}
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
  <div class="modal" id="myModal_addbook">
    <div class="modal-dialog">
      <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
          <h4 class="modal-title">Add Book</h4>
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
                        src="fetchbookimg(this.$route.params.id)"
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
                        >current_book.book_name : current_book.title
                        current_book.status
                      </a>
                    </p>

                    <!-- Text -->
                    <div class="fs-sm text-muted">
                      Author: current_book.author <br />
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
                    <span>Book Name</span>
                    <input
                      type="text"
                      class="ms-auto fs-sm mx-2 form-control form-control-sm"
                      style="width: 120px"
                      id="bookname"
                      required
                    />
                  </li>
                  <li class="list-group-item d-flex">
                    <span>Author</span>
                    <input
                      type="text"
                      class="ms-auto fs-sm mx-2 form-control form-control-sm"
                      style="width: 120px"
                      id="bookauthor"
                      required
                    />
                  </li>
                  <li class="list-group-item d-flex">
                    <span>Status</span>
                    <input
                      type="text"
                      class="ms-auto fs-sm mx-2 form-control form-control-sm"
                      style="width: 120px"
                      id="bookstatus"
                      required
                    />
                  </li>
                  <li class="list-group-item d-flex">
                    <span>Description</span>
                    <textarea
                      class="ms-auto fs-sm mx-2 form-control form-control-sm"
                      style="width: 120px"
                      id="bookdescription"
                      required
                    ></textarea>
                  </li>
                  <li class="list-group-item d-flex">
                    <span>Title</span>
                    <input
                      type="text"
                      class="ms-auto fs-sm mx-2 form-control form-control-sm"
                      style="width: 120px"
                      id="bookstatus"
                      required
                    />
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
              After the Return of Date/Time, the book will be automatically
              returned or the access to user will be revoked.
            </p>

            <!-- Button -->
            <!-- <button
              :disabled="!isDateValid"
              class="btn w-100 btn-dark"
              v-on:click="request()"
            >
              Request for Book
            </button> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import NavBar_admin from "@/components/NavBar_admin.vue";
import { API_URL } from "../../constants";
export default {
  name: "AdminDashboardView",
  components: {
    NavBar_admin,
  },
  data() {
    return {
      data: [],
      title: "Add",
      section_id: null,
    };
  },
  beforeCreate() {
    const token = localStorage.getItem("library_management_system_token");
    this.$store.commit("setNav", "dashboard");
    fetch(API_URL + "/admin_dashboard", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": token,
      },
    })
      .then((response) => response.json())
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
    add_section() {
      const section_name = document.getElementById("sectionname").value;
      const description = document.getElementById("sectiondescription").value;
      const token = localStorage.getItem("library_management_system_token");
      fetch(API_URL + "/add_section", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": token,
        },
        body: JSON.stringify({
          section_name: section_name,
          description: description,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          if (data.status != "success") {
            alert(data.message);
          } else {
            alert(data.message);
            window.location.reload();
          }
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
    edit_section() {
      const section_name = document.getElementById("sectionname").value;
      const description = document.getElementById("sectiondescription").value;
      const token = localStorage.getItem("library_management_system_token");
      fetch(API_URL + "/edit_section", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": token,
        },
        body: JSON.stringify({
          section_name: section_name,
          description: description,
          section_id: this.section_id,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          if (data.status != "success") {
            alert(data.message);
          } else {
            alert(data.message);
            window.location.reload();
          }
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
    delete_section(id) {
      const token = localStorage.getItem("library_management_system_token");
      fetch(API_URL + "/delete_section", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": token,
        },
        body: JSON.stringify({
          section_id: id,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          if (data.status != "success") {
            alert(data.message);
          } else {
            alert(data.message);
            window.location.reload();
          }
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
    edit_section_name(id) {
      this.title = "Edit";
      this.section_id = id;
    },
    add_section_name() {
      this.title = "Add";
    },
    istitle() {
      if (this.title == "Add") {
        return false;
      } else {
        return true;
      }
    },
  },
};
</script>
