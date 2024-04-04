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
        await axios.post(API_URL + "/addbooks", formData); // Adjust the URL as per your backend API
        alert("Data uploaded successfully!");
      } catch (error) {
        console.error("Error uploading data:", error);
      }
    },
  },
};
</script>
