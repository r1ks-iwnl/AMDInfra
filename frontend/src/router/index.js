import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const routes = [
  { path: '/runs', name: 'runs', component: () => import('../views/RunsList.vue'), meta: { requiresAuth: true} },
  { path: '/runs/:id', name: 'run-detail', component: () => import('../views/RunDetail.vue'), meta: { requiresAuth: true}},
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { name: 'login' }
  }
  if (to.name === 'login' && auth.isLoggedIn) {
    return { name: 'runs' }
  }
})

export default router
