import { defineStore } from 'pinia'

function decodeJWT(token){
  try {
    const parts = token.split('.')
    if(parts.length !== 3) return null
    const payload = JSON.parse(atob(parts[1]))
    return payload
  }
  catch(e) {
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => {
    // localStorage tokens are used for ease of developement
    // this is a XSS vulnerability and in production should be replaced with HttpOnly cookies
    const token = localStorage.getItem('access_token') || null

    return {
      token,
      user: token ? { email: decodeJWT(token)?.sub } : null,
      authError: null
    }
  },
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    login(token) {
      this.token = token
      this.authError = null
      const decoded = decodeJWT(token)
      this.user = { email: decoded?.sub || "Couldn't retrieve email" }
      localStorage.setItem('access_token', token)
    },
    logout(errorMsg = null) {
      this.token = null
      this.user = null
      this.authError = errorMsg
      localStorage.removeItem('access_token')
    },
  },
})
