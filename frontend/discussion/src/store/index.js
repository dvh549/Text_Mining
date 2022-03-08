import { createStore } from 'vuex'

export default createStore({
  state: {
    username: null
  },
  getters: {
    getUsername(state){
      return state.username
    },
  },
  mutations: {
    setUsername(state, username){
      state.username = username
    },
  },
  actions: {
  },
  modules: {
  }
})
