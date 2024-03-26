<!-- <template>
  <div class="home">
    <NavBar msg="Welcome to Your Vue.js App" />
    <img alt="Vue logo" src="../assets/logo.png" />
    <h1>User Dashboard</h1>
  </div>
</template>

<script>
// @ is an alias to /src
import NavBar from "@/components/NavBar.vue";

export default {
  name: "HomeView",
  beforeCreate: async function () {
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
        if (data.status != "success") {
          localStorage.removeItem("library_management_system_token");
          localStorage.removeItem("username");
          this.$router.push("/signin");
        }
      });
  },
};
</script> -->
