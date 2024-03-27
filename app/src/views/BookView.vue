<template>
  <div class="book">
    <NavBar msg="Welcome to Your Vue.js App" />
    <!-- <h1>Book Dashboard</h1> -->
  </div>
  <div class="container-fluid text-center" style="margin-top: 2%;">
    <div class="row">
      <div class="col-md-3 order-md-last">
        <!-- last col -->
        <div class="card mx-2" style="width: 100%">
          <img
            :src="fetchbookimg(this.$route.params.id)"
            class="card-img-top my-2"
            style="width: 10px; height: 10px"
            alt="..."
          />
          <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <p class="card-text">
              3 Some quick example text to build on the card title and make up
              the bulk of the card's content.
            </p>
            <a href="#" class="btn fw-medium d align-items-center justify-content-center" style="background-color: rgb(253, 147, 24); border-radius: 20px;">Request for Book</a>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card mx-2" style="width: 100%">
          <div class="card-body">
            <p
              class="fs-3 fw-semibold text-justify-center my-0"
              style="text-align: left"
            >
              Chemistry: The Central Science in SI Units, Expanded Edition,
              Global Edition
            </p>
            <p
              class="text-justify-center"
              style="text-align: left; color: gray"
            >
              By: Theodore L. Brown, H. Eugene LeMay, Bruce E. Bursten,
              Catherine Murphy, Patrick Woodward, Matthew E. Stoltzfus
            </p>
            <hr />
            <p
              class="fw-medium text-justify-center my-0"
              style="text-align: left; color: black; font-size: 15px"
            >
              For courses intwo-semester general chemistry. <br />
            </p>
            <p
              class="fw-semibold text-justify-center my-0"
              style="text-align: left; color: black; font-size: 15px"
            >
              Accurate,data-driven authorship with expanded interactivity leads
              to greater studentengagement
            </p>
            <br />
            <p
              class="fw-medium text-justify-center my-0"
              style="text-align: left; color: black; font-size: 15px"
            >
              Unrivaled problem sets, notablescientific accuracy and currency,
              and remarkable clarity have made Chemistry:The Central Science the
              leading general chemistry text for more than adecade. Trusted,
              innovative, and calibrated, the text increases
              conceptualunderstanding and leads to greater student success in
              general chemistry bybuilding on the expertise of the dynamic
              author team of leading researchers andaward-winning teachers.
              MasteringTM Chemistryis not included. Students, if Mastering is
              arecommended/mandatory component of the course, please ask your
              instructor forthe correct ISBN and course ID. Mastering should
              only be purchased whenrequired by an instructor. Instructors,
              contact your Pearson rep for moreinformation. Mastering is an
              online homework,tutorial, and assessment product designed to
              personalize learning and improveresults. With a wide range of
              interactive, engaging, and assignable activities,students are
              encouraged to actively learn and retain tough course concepts.
            </p>
            <a href="#" class="btn fw-medium d align-items-center justify-content-center" style="background-color: rgb(254, 210, 19); border-radius: 20px;margin-top: 20px;">Add To Wishlist</a>
          </div>
        </div>
      </div>
      <div class="col-md-3 order-md-first">
        <div class="mx-2">
          <img
            :src="fetchbookimg(this.$route.params.id)"
            class="card-img-top mx-2"
            style="width: 100%; height: 500px"
            alt="..."
          />
        </div>
      </div>
    </div>
    <div class="container mx-4">
      <hr style="width: 93%;">
    <p
              class="fw-semibold text-justify-center my-0"
              style="text-align: left; color: black; font-size: 20px"
            >
              Recommandation
            </p>
          </div>
          <div class="row">
        <div class="col-12" style="margin-top: 20px;">
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
      current_book: null,
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
          this.current_book=data.current_book;
        }
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
  },
};
</script>
<style></style>
