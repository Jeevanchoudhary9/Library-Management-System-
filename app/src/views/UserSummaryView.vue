<template>
  <div>
    <NavBar_admin msg="Welcome to Your Vue.js App" />
    <div style="display: flex; justify-content: flex-end; margin-bottom: 20px">
      <button
        @click="printPage"
        class="btn btn-primary rounded"
        style="width: 50px; margin-right: 30px; margin-bottom: 0px"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-6 h-6"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M6.72 13.829c-.24.03-.48.062-.72.096m.72-.096a42.415 42.415 0 0110.56 0m-10.56 0L6.34 18m10.94-4.171c.24.03.48.062.72.096m-.72-.096L17.66 18m0 0l.229 2.523a1.125 1.125 0 01-1.12 1.227H7.231c-.662 0-1.18-.568-1.12-1.227L6.34 18m11.318 0h1.091A2.25 2.25 0 0021 15.75V9.456c0-1.081-.768-2.015-1.837-2.175a48.055 48.055 0 00-1.913-.247M6.34 18H5.25A2.25 2.25 0 013 15.75V9.456c0-1.081.768-2.015 1.837-2.175a48.041 48.041 0 011.913-.247m10.5 0a48.536 48.536 0 00-10.5 0m10.5 0V3.375c0-.621-.504-1.125-1.125-1.125h-8.25c-.621 0-1.125.504-1.125 1.125v3.659M18 10.5h.008v.008H18V10.5zm-3 0h.008v.008H15V10.5z"
          />
        </svg>
      </button>
    </div>
    <div class="row">
      <canvas
        id="bookIssuanceChart"
        width="800"
        height="400"
        style="max-height: 600px; max-width: 600px; margin: 50px"
      ></canvas>
      <canvas
        id="SectionIssuanceChart"
        width="800"
        height="400"
        style="max-height: 600px; max-width: 600px; margin: 50px"
      ></canvas>
      <canvas
        id="statusIssuanceChart"
        width="800"
        height="400"
        style="max-height: 600px; max-width: 600px; margin: 50px"
      ></canvas>
    </div>
  </div>
</template>

<script>
import NavBar_admin from "@/components/NavBar_admin.vue";
import Chart from "chart.js/auto";
import { API_URL } from "../../constants";

export default {
  name: "AdminSummaryView",
  components: {
    NavBar_admin,
  },
  beforeCreate() {
    const token = localStorage.getItem("library_management_system_token");
    this.$store.commit("setNav", "Summary");
    fetch(API_URL + "/usersummary", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": token,
      },
    })
      .then((response) => {
        if (response.status == 401) {
          this.$router.push("/unauthorized");
        } else {
          return response.json();
        }
      })
      .then((data) => {
        this.$store.commit("setUser", data.current_user.username);
        this.$store.commit("setNav", "Summary");
        console.log(data);
        this.books = data.books;
        this.bookcount = data.books_count;
        this.sectionData = data.sections_name;
        this.sectioncount = data.sections_count;
        this.bookData = {
          labels: this.books,
          issuances: this.bookcount,
        };
        this.renderChart();
        this.sectionData = {
          labels: data.sections_name,
          issuances: data.sections_count,
        };
        this.renderSectionChart();
        this.statusData = {
          labels: data.status_name,
          issuances: data.status_count,
        };
        this.renderstatusChart();
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  },
  data() {
    return {
      bookData: {},
      chart: null,
      books: [],
      bookcount: [],
      sectionData: [],
      sectioncount: [],
      sectionchart: null,
      statusData: [],
      statuscount: [],
      statuschart: null,
    };
  },
  mounted() {},
  methods: {
    printPage() {
      window.print();
    },
    renderChart() {
      if (this.chart) {
        this.chart.destroy();
      }

      const ctx = document.getElementById("bookIssuanceChart").getContext("2d");
      this.chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: this.bookData.labels,
          datasets: [
            {
              label: "Number of Issuances",
              data: this.bookData.issuances,
              backgroundColor: [
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)",
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(153, 102, 255, 0.2)",
              ],
              borderColor: [
                "rgba(255, 99, 132, 1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(153, 102, 255, 1)",
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Number of Issuances",
              },
            },
            x: {
              title: {
                display: true,
                text: "Book Name",
              },
            },
          },
        },
      });
    },
    renderSectionChart() {
      if (this.sectionchart) {
        this.sectionchart.destroy();
      }

      const ctx = document
        .getElementById("SectionIssuanceChart")
        .getContext("2d");
      this.sectionchart = new Chart(ctx, {
        type: "pie",
        data: {
          labels: this.sectionData.labels,
          datasets: [
            {
              label: "Number of Issuances",
              data: this.sectionData.issuances,
              backgroundColor: [
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)",
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(153, 102, 255, 0.2)",
              ],
              borderColor: [
                "rgba(255, 99, 132, 1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(153, 102, 255, 1)",
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Number of Issuances",
              },
            },
            x: {
              title: {
                display: true,
                text: "Section Name",
              },
            },
          },
        },
      });
    },
    renderstatusChart() {
      if (this.statuschart) {
        this.statuschart.destroy();
      }

      const ctx = document
        .getElementById("statusIssuanceChart")
        .getContext("2d");
      this.statuschart = new Chart(ctx, {
        type: "line",
        data: {
          labels: this.statusData.labels,
          datasets: [
            {
              label: "Number of Issuances",
              data: this.statusData.issuances,
              backgroundColor: [
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)",
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(153, 102, 255, 0.2)",
              ],
              borderColor: [
                "rgba(255, 99, 132, 1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(153, 102, 255, 1)",
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Number of Issuances",
              },
            },
            x: {
              title: {
                display: true,
                text: "Status",
              },
            },
          },
        },
      });
    },
  },
};
</script>
