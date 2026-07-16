<script setup>
import { getLoginUrl } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const allowedOrigin = import.meta.env.VITE_API_ORIGIN

function handleLogin() {
  const width = 500, height = 600
  const left = window.screen.width / 2 - width / 2
  const top = window.screen.height / 2 - height / 2

  const popup = window.open(
    getLoginUrl,
    'Google Login',
    `width=${width},height=${height},left=${left},top=${top}`
  )

  if (!popup) {
    auth.authError = 'Popup was blocked. Please allow popups and try again.'
    return
  }

  window.addEventListener('message', (event) => {
    if (event.origin !== allowedOrigin) {
      console.warn(
        `Login origin mismatch. Expected: ${allowedOrigin}, got: ${event.origin}. ` +
        `Check API_ORIGIN env var.`
      )
      auth.authError = 'Login failed.'
      popup.close()
      return
    }
    if (event.data && event.data.token) {
      auth.login(event.data.token)
      popup.close()
      router.push(route.query.redirect || '/runs')
    }
  }, { once: true })
}
</script>

<template>
  <div class="auth-bar">
    <button v-if="!auth.isLoggedIn" @click="handleLogin" class="btn-login">
      Log In
    </button>
    <div v-if="auth.authError" class="state-box">
      <div class="error-state">
        <h3>{{ auth.authError }}</h3>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-bar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  justify-content: center;
  align-items: center;
  margin: 1.5rem 0;
}

.state-box {
  text-align: center;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: var(--color-text-secondary);
}

.error-state { color: var(--color-warning); }

.btn-login {
  display: inline-block;
  background-color: var(--color-bg-dark);
  color: #ffffff;
  font-weight: 600;
  font-size: 1rem;
  font-family: inherit;
  padding: 8px 18px;
  border-radius: 6px;
  border: 1px solid var(--color-grid-line);
  cursor: pointer;
}

.btn-login:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}
</style>
