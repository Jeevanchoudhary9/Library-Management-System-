<template>
  <div>
    <nav-bar />
    <div>
      <embed
        type="application/pdf"
        src="http://127.0.0.1:5000/api/pdfshow#toolbar=0&navpanes=0&scrollbar=0"
        style="width: 100%; height: 93.8vh"
        toolbar="0"
        download="false"
        oncontextmenu="return false;"
        disableprint="true"
        />
    </div>
  </div>
</template>
<script>
// import { API_URL } from "../../constants";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "BookRead",
  components: {
    NavBar,
  },
  data() {
    return {
      pdfContent: "",
    };
  },
  //   beforeCreate() {
  //     const token = localStorage.getItem("library_management_system_token");
  //     this.$store.commit("setNav", "Reading Book");
  //     fetch(API_URL + "/bookread/" + this.$route.params.id, {
  //       method: "GET",
  //       headers: {
  //         "Content-Type": "application/json",
  //         "x-access-token": token,
  //       },
  //     })
  //       .then((response) => {
  //         console.log(response);
  //         if (response.status == 401) {
  //           console.log("1");
  //           this.$router.push("/unauthorized");
  //         } else {
  //           console.log("2");
  //           return response.json();
  //         }
  //       })
  //       .then((data) => {
  //         this.$store.commit("setUser", data.user_data.username);
  //         if (data.status !== "success") {
  //           alert(data.message);
  //           this.$router.push("/");
  //         } else {
  //           this.$store.commit("setUser", data.user_data.username);
  //           this.$store.commit("setNav", "Reading Book");
  //           console.log(data);
  //           this.pdfContent = data.pdf_content;
  //         }
  //       })
  //       .catch((error) => {
  //         console.error("Error fetching data:", error);
  //         this.$router.push("/signin");
  //       });
  //   },
};
</script>
