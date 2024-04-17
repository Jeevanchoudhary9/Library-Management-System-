<template>
  <div>
    <nav-bar />
    <div>
      <embed
        type="application/pdf"
        :src="url"
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
import { API_URL } from "../../constants";
import NavBar from "@/components/NavBar_admin.vue";
export default {
  name: "AdminBookRead",
  components: {
    NavBar,
  },
  data() {
    return {
      pdfContent: "",
      url:
        API_URL +
        "/pdfshow/" +
        this.$route.params.id +
        "/" +
        localStorage.getItem("library_management_system_token"),
    };
  },
};
</script>
