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
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="2"
                stroke="currentColor"
                style="width: 20px; height: 20px"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125"
                />
              </svg>
            </button>
            <button
              class="btn btn-primary btn-block mx-1"
              data-bs-toggle="modal"
              data-bs-target="#myModal_addbook"
              v-on:click="edit_section_name(sec[0][0].section_id)"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="3"
                stroke="currentColor"
                style="width: 20px; height: 20px"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M12 4.5v15m7.5-7.5h-15"
                />
              </svg>
            </button>
            <button
              class="btn btn-danger btn-block mx-1"
              v-on:click="delete_section(sec[0][0].section_id)"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="2"
                stroke="currentColor"
                style="width: 20px; height: 20px"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
                />
              </svg>
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
            style="height: 484px; overflow-x: auto; margin-right: 200px"
          >
            <ol class="list-unstyled d-flex">
              <li
                class="mx-4"
                v-for="books in sec[1]"
                :key="books.book_id"
                style="width: 202px"
              >
                <div>
                  <button
                    class="btn btn-warning btn-block mb-2 mx-1"
                    v-on:click="edit_book_data(books, books.book_id)"
                    data-bs-toggle="modal"
                    data-bs-target="#myModal_editbook"
                  >
                    Edit
                  </button>
                  <button
                    class="btn btn-danger btn-block mb-2 mx-1"
                    v-on:click="delete_book(books.book_id)"
                  >
                    Delete
                  </button>
                </div>
                <a
                  class=""
                  :href="'/adminbook/' + books.book_id"
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

  <!-- Modals -->
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
                    <!-- <a href="">
                      <input
                        type="file"
                        ref="fileInput"
                        @change="handleFileUpload"
                      />
                      <input
                        type="file"
                        class="mx-2"
                        style="width: 90px; height: 110px"
                        alt="..."
                      />
                    </a> -->
                    <div>
                      <label
                        :key="photoURL"
                        @change="renderImage($event.target.files[0])"
                        class="file-input-label border d-flex justify-content-between align-items-center"
                        style="
                          max-width: 90px;
                          max-height: 110px;
                          width: 90px;
                          height: 110px;
                        "
                        :style="{
                          backgroundImage: `url(${photoURL})`,
                          backgroundSize: 'cover',
                          backgroundPosition: 'center',
                          width: '90px',
                          height: '110px',
                        }"
                      >
                        <input
                          type="file"
                          ref="fileInput"
                          @change="handleFileUpload"
                          style="display: none"
                          required
                        />
                        Upload Photo
                      </label>
                    </div>
                  </div>
                  <div class="col">
                    <!-- Title -->
                    <p class="fs-sm fw-bold">
                      <a class="text-body" href="product.html"
                        >{{ formData.book_name }} : {{ formData.title }}
                      </a>
                    </p>

                    <!-- Text -->
                    <div class="fs-sm text-muted">
                      Author: {{ formData.author }} <br />
                      Pages: 1000
                    </div>
                  </div>
                  <div class="col" hidden>
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
                    <span>Upload PDF</span>
                    <input
                      type="file"
                      class="ms-auto fs-sm mx-2 form-control form-control-sm"
                      style="width: 120px"
                      ref="fileInputpdf"
                      @change="handleFileUploadpdf"
                      required
                    />
                  </li>
                  <li class="list-group-item d-flex">
                    <span>Book Name</span>
                    <input
                      type="text"
                      class="ms-auto fs-sm mx-2 form-control form-control-sm"
                      style="width: 120px"
                      id="bookname"
                      v-model="formData.book_name"
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
                      v-model="formData.author"
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
                      v-model="formData.status"
                      required
                    />
                  </li>
                  <li class="list-group-item d-flex">
                    <span>Description</span>
                    <textarea
                      class="ms-auto fs-sm mx-2 form-control form-control-sm"
                      style="width: 120px"
                      id="bookdescription"
                      v-model="formData.description"
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
                      v-model="formData.title"
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
              Every field is required and photo must be in jpeg format.
            </p>

            <!-- Button -->
            <button
              class="btn w-100 btn-dark"
              v-on:click="uploadData(section_id)"
            >
              Add Book
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="modal" id="myModal_editbook">
    <div class="modal-dialog">
      <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
          <h4 class="modal-title">Edit Book</h4>
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
                    <!-- <a href="">
                      <input
                        type="file"
                        ref="fileInput"
                        @change="handleFileUpload"
                      />
                      <input
                        type="file"
                        class="mx-2"
                        style="width: 90px; height: 110px"
                        alt="..."
                      />
                    </a> -->
                    <div>
                      <label
                        :key="anotherPhotoURL"
                        @change="renderAnotherImage($event.target.files[0])"
                        class="file-input-label border d-flex justify-content-between align-items-center"
                        style="
                          max-width: 90px;
                          max-height: 110px;
                          width: 90px;
                          height: 110px;
                        "
                        :style="{
                          backgroundImage: `url(${anotherPhotoURL})`,
                          backgroundSize: 'cover',
                          backgroundPosition: 'center',
                          width: '90px',
                          height: '110px',
                        }"
                      >
                        <input
                          type="file"
                          ref="anotherFileInput"
                          @change="handleAnotherFileUpload"
                          style="display: none"
                        />
                        Upload Another Photo
                      </label>
                    </div>
                  </div>
                  <div class="col">
                    <!-- Title -->
                    <p class="fs-sm fw-bold">
                      <a class="text-body" href="product.html"
                        >{{ formData.book_name }} : {{ formData.title }}
                      </a>
                    </p>

                    <!-- Text -->
                    <div class="fs-sm text-muted">
                      Author: {{ formData.author }} <br />
                      Pages: 1000
                    </div>
                  </div>
                  <div class="col" hidden>
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
                    <span>Upload PDF</span>
                    <input
                      type="file"
                      class="ms-auto fs-sm mx-2 form-control form-control-sm"
                      style="width: 120px"
                      ref="anotherFileInputpdf"
                      @change="handleAnotherFileUploadpdf"
                      required
                    />
                  </li>
                  <li class="list-group-item d-flex">
                    <span>Book Name</span>
                    <input
                      type="text"
                      class="ms-auto fs-sm mx-2 form-control form-control-sm"
                      style="width: 120px"
                      id="bookname"
                      v-model="formData.book_name"
                      required
                    />
                  </li>
                  <li class="list-group-item d-flex">
                    <span>Section Id</span>
                    <input
                      type="text"
                      class="ms-auto fs-sm mx-2 form-control form-control-sm"
                      style="width: 120px"
                      id="sectionid"
                      v-model="formData.section_id"
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
                      v-model="formData.author"
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
                      v-model="formData.status"
                      required
                    />
                  </li>
                  <li class="list-group-item d-flex">
                    <span>Description</span>
                    <textarea
                      class="ms-auto fs-sm mx-2 form-control form-control-sm"
                      style="width: 120px"
                      id="bookdescription"
                      v-model="formData.description"
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
                      v-model="formData.title"
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
              Every field is required and photo must be in jpeg format.
            </p>

            <!-- Button -->
            <button class="btn w-100 btn-dark" v-on:click="uploadDataedit()">
              Edit Book
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import NavBar_admin from "@/components/NavBar_admin.vue";
import axios from "axios"; // Import axios library
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
      file: null,
      filepdf: null,
      anotherFile: null,
      anotherFilepdf: null,
      photoURL: "",
      anotherPhotoURL: "",
      formData: {
        book_id: null,
        book_name: "",
        author: "",
        section_id: "",
        status: "",
        description: "",
        title: "",
      },
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
    edit_book_data(book, book_id) {
      this.formData.book_id = book_id;
      this.formData.author = book.author;
      this.formData.book_name = book.book_name;
      this.formData.title = book.title;
      this.formData.description = book.description;
      this.formData.status = book.status;
      this.formData.section_id = book.section_id;
      this.edit_add = "Edit";
      this.anotherPhotoURL = API_URL + "/fetchbookimg/" + book.book_id;
    },
    add_book_data(id) {
      this.section_id = id;
      this.formData.book_id = "";
      this.formData.author = "";
      this.formData.book_name = "";
      this.formData.title = "";
      this.formData.description = "";
      this.formData.status = "";
      this.edit_add = "Add";
    },
    delete_section(id) {
      const confirmed = window.confirm(
        "Are you sure you want to delete this section\n" +
          "𝗕𝗼𝗼𝗸𝘀 𝗯𝗲𝗹𝗼𝗻𝗴𝘀 𝘁𝗼 𝘁𝗵𝗶𝘀 𝘀𝗲𝗰𝘁𝗶𝗼𝗻 𝘄𝗶𝗹𝗹 𝗮𝗹𝘀𝗼 𝗯𝗲 𝗱𝗲𝗹𝗲𝘁𝗲𝗱?"
      );
      if (!confirmed) {
        return;
      }
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
    handleFileUpload() {
      this.file = this.$refs.fileInput.files[0];
      this.renderImage(this.file);
    },
    handleFileUploadpdf() {
      this.filepdf = this.$refs.fileInputpdf.files[0];
    },
    renderImage(file) {
      const reader = new FileReader();
      console.log("file", file);
      reader.onload = (e) => {
        this.photoURL = e.target.result;
        console.log("photoURL", this.photoURL);
      };
      reader.readAsDataURL(file);
    },
    async uploadData(section_id) {
      const formData = new FormData();
      console.log(this.file);
      formData.append("image", this.file);
      formData.append("pdf_file", this.filepdf);
      formData.append("book_name", this.formData.book_name);
      formData.append("author", this.formData.author);
      formData.append("section_id", section_id);
      formData.append("status", this.formData.status);
      formData.append("description", this.formData.description);
      formData.append("title", this.formData.title);

      try {
        const response = await axios.post(API_URL + "/add_books", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            "x-access-token": localStorage.getItem(
              "library_management_system_token"
            ),
          },
        });
        if (response.data.status != "success") {
          alert(response.data.message);
        } else {
          alert(response.data.message);
          window.location.reload();
        }
      } catch (error) {
        if (error.response.status == 401) {
          this.$router.push("/unauthorized");
        } else {
          alert(error.response.data.message);
          console.error("Error uploading data:", error);
        }
      }
    },
    handleAnotherFileUpload() {
      this.anotherFile = this.$refs.anotherFileInput.files[0];
      this.renderAnotherImage(this.anotherFile);
    },
    renderAnotherImage(anotherFile) {
      const reader = new FileReader();
      console.log("file", anotherFile);
      reader.onload = (e) => {
        this.anotherPhotoURL = e.target.result;
        console.log("anotherPhotoURL", this.anotherPhotoURL);
      };
      reader.readAsDataURL(anotherFile);
    },
    handleAnotherFileUploadpdf() {
      this.anotherFilepdf = this.$refs.anotherFileInputpdf.files[0];
      console.log(this.anotherFilepdf);
    },
    async uploadDataedit() {
      const formData = new FormData();
      if (this.anotherFile != null) {
        formData.append("image", this.anotherFile);
      } else {
        formData.append("image", "");
      }
      if (this.anotherFilepdf != null) {
        formData.append("pdf_file", this.anotherFilepdf);
      } else {
        formData.append("pdf_file", "");
      }
      // if (this.anotherFile != null && this.anotherFilepdf != null) {
      //   formData.append("image", this.anotherFile);
      //   formData.append("pdf_file", this.anotherFilepdf);
      //   console.log(this.anotherFilepdf);
      // } else {
      //   formData.append("image", "");
      //   formData.append("pdf_file", "");
      // }
      console.log(this.anotherFile, this.anotherFilepdf);
      formData.append("book_id", this.formData.book_id);
      formData.append("book_name", this.formData.book_name);
      formData.append("author", this.formData.author);
      formData.append("section_id", this.formData.section_id);
      formData.append("status", this.formData.status);
      formData.append("description", this.formData.description);
      formData.append("title", this.formData.title);
      console.log(this.formData);
      try {
        const response = await axios.post(API_URL + "/edit_book", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            "x-access-token": localStorage.getItem(
              "library_management_system_token"
            ),
          },
        });
        // get message from backend
        if (response.data.status != "success") {
          alert(response.data.message);
        } else {
          alert(response.data.message);
          window.location.reload();
        }
      } catch (error) {
        if (error.response.status == 401) {
          this.$router.push("/unauthorized");
        }
        alert(error.response.data.message);
        console.error("Error uploading data:", error);
      }
    },
    edit_section_name(id) {
      this.title = "Edit";
      this.section_id = id;
      this.formData.book_id = "";
      this.formData.author = "";
      this.formData.book_name = "";
      this.formData.title = "";
      this.formData.description = "";
      this.formData.status = "";
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
    delete_book(bookid) {
      const confirmed = window.confirm(
        "Are you sure you want to delete this book\n" + "𝗕𝗼𝗼𝗸 𝘄𝗶𝗹𝗹 𝗯𝗲 𝗱𝗲𝗹𝗲𝘁𝗲𝗱?"
      );
      if (!confirmed) {
        return;
      }
      const token = localStorage.getItem("library_management_system_token");
      fetch(API_URL + "/delete_book", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": token,
        },
        body: JSON.stringify({
          book_id: bookid,
        }),
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
  },
};
</script>
