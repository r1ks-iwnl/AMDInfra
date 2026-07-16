import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import router from '@/router'

const api = axios.create({
  baseURL: '/api',
})

api.interceptors.request.use(
  (config) => {
    const auth = useAuthStore()

    if (auth.token) {
      config.headers.Authorization = `Bearer ${auth.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if(err.response?.status === 401) {
      const auth = useAuthStore()
      auth.logout("Session expired.")
      router.push('/login')
    }
    return Promise.reject(err)
  }
)

export const getLoginUrl = `${api.defaults.baseURL}/auth/login`

export default api
