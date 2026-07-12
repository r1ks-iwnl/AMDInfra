import axios from 'axios'

const api = axios.create({
  // By using a relative path starting with /api,
  // Axios will automatically call http://localhost:5173/api/...
  baseURL: '/',
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default api
