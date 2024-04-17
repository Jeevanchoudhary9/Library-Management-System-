<template>
  <div class="book">
    <NavBar_admin msg="Welcome to Your Vue.js App" />
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
          </div>
        </div>
      </div>
      <div class="col-md-3 order-md-last">
        <!-- last col -->
        <div class="card mx-2" style="width: 100%">
          <div class="card-body">
            <h5 class="card-title">View for Book</h5>
            <p class="card-text">
              View for the book to read it. The book will be available for you
              to read for the period of time you requested after approval.
            </p>
            <a
              :href="'/bookreadadmin/' + this.$route.params.id"
              class="btn fw-medium d align-items-center justify-content-center"
              style="background-color: rgb(253, 147, 24); border-radius: 20px"
              >View for Book</a
            >
          </div>
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
import NavBar_admin from "@/components/NavBar_admin.vue";
import { API_URL } from "../../constants";
export default {
  name: "AdminBookView",
  data() {
    return {
      data: [],
      current_book: [],
    };
  },
  beforeCreate() {
    const token = localStorage.getItem("library_management_system_token");
    this.$store.commit("setNav", "books");
    fetch(API_URL + "/adminbook/" + this.$route.params.id, {
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
          console.log(data);
          this.current_book = data.current_book;
          if (data.issue == "Requested") {
            this.status = "Cancel Request";
          }
          if (data.issue == "Issued") {
            this.status = "Return Book";
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
    NavBar_admin,
  },
  methods: {
    fetchbookimg(bookId) {
      return API_URL + "/fetchbookimg/" + bookId;
    },
  },
  computed: {},
  mounted() {},
  beforeUnmount() {},
};
</script>
<style></style>
