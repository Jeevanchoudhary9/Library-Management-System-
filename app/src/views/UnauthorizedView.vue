<template>
  <div>
    <h1>Unauthorized</h1>
    <p>You are not authorized to view this page.</p>
    <button @click="this.$router.push('/signin')" class="btn btn-primary">
      Home Page
    </button>
  </div>
</template>
<script>
import { API_URL } from "../../constants";

export default {
  name: "UnauthorizedView",
  beforeCreate() {
    const token = localStorage.getItem("library_management_system_token");
    fetch(API_URL + "/verify_user", {
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
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  },
};
</script>
