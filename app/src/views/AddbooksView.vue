<template>
  <NavBar msg="Welcome to Library Management System" />
  <div>
    <input type="file" ref="fileInput" @change="handleFileUpload" />
    <input type="text" v-model="formData.book_name" placeholder="Book Name" />
    <input type="text" v-model="formData.author" placeholder="Author" />
    <input
      type="number"
      v-model="formData.section_id"
      placeholder="Section ID"
    />
    <input type="text" v-model="formData.status" placeholder="Status" />
    <!-- <input
      type="textarea"
      v-model="formData.description"
      placeholder="Description"
    /> -->
    <textarea v-model="formData.description"></textarea>
    <input type="text" v-model="formData.title" placeholder="Title" />
    <button @click="uploadData">Upload</button>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import axios from "axios"; // Import axios library
import { API_URL } from "../../constants"; // Assuming API_URL is defined in constants.js

export default {
  name: "AddbooksView",
  components: {
    NavBar,
  },
  data() {
    return {
      file: null,
      formData: {
        book_name: "",
        author: "",
        section_id: "",
        status: "",
        description: "",
        title: "",
      },
    };
  },
  methods: {
    handleFileUpload() {
      this.file = this.$refs.fileInput.files[0];
    },
    async uploadData() {
      const formData = new FormData();
      formData.append("image", this.file);
      formData.append("book_name", this.formData.book_name);
      formData.append("author", this.formData.author);
      formData.append("section_id", this.formData.section_id);
      formData.append("status", this.formData.status);
      formData.append("description", this.formData.description);
      formData.append("title", this.formData.title);

      try {
        // Send a POST request to the API endpoint
        const token = localStorage.getItem("library_management_system_token");
        try {
          const response = await axios.post(API_URL + "/add_books", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
              "x-access-token": token,
            },
          });

          // Log response for debugging

          // Check for response status and handle accordingly
          if (response.data.status !== "success") {
            // Unauthorized or other error status
            console.log("Error:", response.data.message);
            localStorage.removeItem("library_management_system_token");
            this.$router.push("/signin");
          } else {
            // Success response
            console.log("Success:", response.data.message);
            alert(response.data.message);
          }
        } catch (error) {
          if (error.response.status == 401) {
            this.$router.push("/unauthorized");
          }
          console.error("Error uploading data:", error);
          // Handle network errors or other errors here
        }
      } catch (error) {
        console.error("Error uploading data:", error);
      }
    },
  },
};
</script>
