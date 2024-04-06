<template>
  <section
    class="vh-100 bg-image"
    :style="{
      backgroundImage: 'url(' + require('@/assets/img/books.png') + ')',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }"
  >
    <div class="mask d-flex align-items-center h-100 gradient-custom-3">
      <div class="container h-100">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col-12 col-md-9 col-lg-7 col-xl-6">
            <div class="card" style="border-radius: 15px">
              <div class="card-body p-5">
                <h2 class="text-uppercase text-center mb-5">Login</h2>

                <form>
                  <div class="form-outline mb-4">
                    <input
                      type="text"
                      name="username"
                      v-model="username"
                      id="username"
                      class="form-control form-control-lg"
                      placeholder="Username"
                      required
                    />
                  </div>
                  <div class="form-outline mb-4">
                    <input
                      type="password"
                      name="password"
                      v-model="password"
                      id="password"
                      class="form-control form-control-lg"
                      placeholder="Password"
                      required
                    />
                  </div>

                  <div class="d-flex justify-content-center">
                    <button
                      type="submit"
                      class="btn btn-success btn-block btn-lg gradient-custom-4 text-body"
                      @click.prevent="user_login"
                    >
                      Login
                    </button>
                  </div>

                  <p class="text-center text-muted mt-5 mb-0">
                    Don't have an account?
                    <a href="/signup" class="fw-bold text-body"
                      ><u>Register here</u></a
                    >
                  </p>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
import { API_LOGIN, API_TOKEN_VERIFY } from "../../constants";
export default {
  name: "SiginView",
  beforeCreate: function () {
    const token = localStorage.getItem("library_management_system_token");
    // make an api call to check if the token is valid
    fetch(API_TOKEN_VERIFY, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status == "success" && data.user.role != "admin") {
          this.$router.push("/");
        } else if (data.status == "success" && data.user.role == "admin") {
          this.$router.push("/admin_dashboard");
        }
      });
  },
  data() {
    return {
      username: "",
      password: "",
      message: "",
      message_type: "alert-warning",
    };
  },
  methods: {
    user_login() {
      fetch(API_LOGIN, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status == "success" && data.user_data.role != "admin") {
            localStorage.setItem("library_management_system_token", data.token);
            this.$store.commit("setUser", data.user_data.username);
            this.$router.push("/");
          } else if (
            data.status == "success" &&
            data.user_data.role == "admin"
          ) {
            localStorage.setItem("library_management_system_token", data.token);
            this.$store.commit("setUser", data.user_data.username);
            this.$router.push("/admin_dashboard");
          } else {
            alert(data.message);
          }
        });
    },
  },
  computed: {
    show_message() {
      return this.message != "";
    },
  },
};
</script>
<style>
@import "~bootstrap/dist/css/bootstrap.min.css";
.bg-image {
  height: 100vh;
  background-size: cover;
  background-position: center;
}
</style>
