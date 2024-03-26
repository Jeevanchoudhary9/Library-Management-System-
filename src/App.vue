<template>
  <div>
    <div v-if="api_available">
      <router-view />
    </div>
    <div v-else>
      <div class="alert alert-danger">
        <h1>API is not available</h1>
        <p>Please check your internet connection and try again</p>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
<script>
import axios from "axios";
import { API_URL } from "../constants";
export default {
  name: "App",
  data() {
    return {
      api_available: true,
    };
  },
  created: function () {
    axios
      .get(API_URL + "/apiCheck")
      .then(() => {
        this.api_available = true;
      })
      .catch(() => {
        this.api_available = false;
      });
  },
};
</script>
