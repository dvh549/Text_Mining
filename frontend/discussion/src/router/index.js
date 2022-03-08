import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Discuss from '../views/discuss.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/Discuss',
    name: 'Discuss',
    component: Discuss
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
