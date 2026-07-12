import { createRouter, createWebHistory } from 'vue-router'
import RunsList from '../views/RunsList.vue'

const routes = [
  { path: '/runs', name: 'runs', component: RunsList },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
