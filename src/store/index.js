import { createStore } from "vuex";

const userData = JSON.parse(localStorage.getItem("userData")) || null;
const navData = JSON.parse(localStorage.getItem("navData")) || null;

export default createStore({
  state: {
    userData: userData,
    navData: navData,
  },
  mutations: {
    setUser(state, userData) {
      state.userData = userData;
      localStorage.setItem("userData", JSON.stringify(userData));
    },
    setNav(state, navData) {
      state.navData = navData;
      localStorage.setItem("navData", JSON.stringify(navData));
    },
  },
  actions: {
    setUser({ commit }, userData) {
      commit("setUser", userData);
    },
    setNav({ commit }, navData) {
      commit("setNav", navData);
    },
  },
  getters: {
    getUserData: (state) => state.userData,
    getNavData: (state) => state.navData,
  },
});
