import { createRouter, createWebHistory } from 'vue-router'
// import Home from '../views/Home.vue'
import Discuss from '../views/discuss.vue'
import None from '../views/none.vue'
import Race from '../views/race.vue'
import Religion from '../views/religion.vue'
import Disability from '../views/disability.vue'
import Gender from '../views/gender.vue'


const routes = [

  {
    path: '/',
    name: 'Discuss',
    component: Discuss
  },
  {
    path: '/None',
    name: 'None',
    component: None
  },
  {
    path: '/Race',
    name: 'Race',
    component: Race
  },
  {
    path: '/Religion',
    name: 'Religion',
    component: Religion
  },
  {
    path: '/Disability',
    name: 'Disability',
    component: Disability
  },
  {
    path: '/Gender',
    name: 'Gender',
    component: Gender
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
