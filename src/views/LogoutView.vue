<template>
  <div></div>
</template>

<script>
export default {
  mounted() {
    this.logout(); // Automatically logout when the component is mounted
  },
  methods: {
    logout: function () {
      localStorage.removeItem("library_management_system_token");
      localStorage.removeItem("username");
      this.$router.push("/signin"); // Redirect to login page after logout
    },
  },
};
</script>
