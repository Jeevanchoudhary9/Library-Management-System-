<template>
  <div class="book">
    <NavBar msg="Welcome to Your Vue.js App" />
    <h1>Book Dashboard</h1>
    {{ this.$route.params.id }}
  </div>
  {{ data }}
</template>
<script>
import NavBar from "@/components/NavBar.vue";
import { API_URL } from "../../constants";
export default {
  name: "BookView",
  data() {
    return {
      data: [],
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
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  },
  components: {
    NavBar,
  },
};
</script>
