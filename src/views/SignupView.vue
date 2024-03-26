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
                <h2 class="text-uppercase text-center mb-5">
                  Create an account
                </h2>

                <form>
                  <div class="form-outline mb-4 row">
                    <div class="col">
                      <input
                        type="text"
                        name="firstname"
                        v-model="firstname"
                        id="firstname"
                        class="form-control form-control-lg"
                        placeholder="First Name"
                        required
                      />
                    </div>
                    <div class="col">
                      <input
                        type="text"
                        name="lastname"
                        v-model="lastname"
                        id="lastname"
                        class="form-control form-control-lg"
                        placeholder="Last Name"
                        required
                      />
                    </div>
                  </div>

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
                  <div class="form-outline mb-4 row">
                    <div class="col">
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
                    <div class="col">
                      <input
                        type="password"
                        name="confirm_password"
                        v-model="confirm_password"
                        id="confirmpassword"
                        class="form-control form-control-lg"
                        placeholder="Confirm Password"
                        required
                      />
                    </div>
                  </div>
                  <div class="form-outline mb-4 row">
                    <div class="col">
                      <input
                        type="email"
                        name="email"
                        v-model="email"
                        id="email"
                        class="form-control form-control-lg"
                        placeholder="Email"
                        required
                        pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
                        oninvalid="this.setCustomValidity('Invalid email format')"
                        oninput="this.setCustomValidity('')"
                      />
                    </div>
                    <div class="col">
                      <input
                        type="number"
                        name="phone_number"
                        v-model="phone_number"
                        id="phonenumber"
                        class="form-control form-control-lg"
                        placeholder="Phone Number"
                        required
                      />
                    </div>
                  </div>
                  <div class="form-outline mb-4">
                    <input
                      type="text"
                      name="address"
                      v-model="address"
                      id="address"
                      class="form-control form-control-lg"
                      placeholder="Address"
                      required
                    />
                  </div>
                  <div class="form-outline mb-4 row">
                    <div class="col">
                      <label for="fileToUpload">Upload Photo</label>
                    </div>
                    <div class="col">
                      <input
                        type="file"
                        name="fileToUpload"
                        id="fileToUpload"
                        placeholder="photo"
                      />
                    </div>
                  </div>
                  <div class="form-outline mb-4">
                    <!-- upload photo -->
                  </div>
                  <div class="form-check d-flex justify-content-center mb-5">
                    <input
                      class="form-check-input me-2"
                      type="checkbox"
                      value=""
                      id="checkboxagree"
                    />
                    <label class="form-check-label" for="checkboxagree">
                      I agree all statements in
                      <a href="#!" class="text-body"><u>Terms of service</u></a>
                    </label>
                  </div>

                  <div class="d-flex justify-content-center">
                    <button
                      type="submit"
                      class="btn btn-success btn-block btn-lg gradient-custom-4 text-body"
                      @click.prevent="user_register"
                    >
                      Register
                    </button>
                  </div>

                  <p class="text-center text-muted mt-5 mb-0">
                    Have already an account?
                    <a href="/signin" class="fw-bold text-body"
                      ><u>Login here</u></a
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
import "bootstrap";
import { API_REGISTER } from "../../constants";
export default {
  name: "SignupView",
  data() {
    return {
      firstname: "",
      lastname: "",
      username: "",
      password: "",
      confirm_password: "",
      email: "",
      address: "",
      photo: "",
      message: "",
      message_type: "alert-warning",
    };
  },
  methods: {
    user_register() {
      if (this.match) {
        fetch(API_REGISTER, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            firstname: this.firstname,
            lastname: this.lastname,
            username: this.username,
            password: this.password,
            confirm_password: this.confirm_password,
            email: this.email,
            phone_number: this.phone_number,
            address: this.address,
            photo: this.photo,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status == "success") {
              window.location.href = "/signin";
            }
            alert(data.message);
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      } else {
        this.message = "Password does not match";
      }
    },
  },
  computed: {
    match() {
      if (this.password == this.confirm_password && this.password != "") {
        return true;
      } else {
        console.log("Password does not match");
        return false;
      }
    },
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
