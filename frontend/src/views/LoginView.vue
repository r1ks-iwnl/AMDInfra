<script setup>
import { getLoginUrl } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function handleLogin() {
  const width = 500, height = 600
  const left = window.screen.width / 2 - width / 2
  const top = window.screen.height / 2 - height / 2

  const popup = window.open(
    getLoginUrl,
    'Google Login',
    `width=${width},height=${height},left=${left},top=${top}`
  )

  window.addEventListener('message', (event) => {
    if (event.origin !== 'http://localhost:8000') return

    if (event.data && event.data.token) {
      auth.login(event.data.token)
      popup.close()
      router.push('/runs')
    }
  }, { once: true })
}
</script>

<template>
  <div class="auth-bar">
    <button @click="handleLogin" class="btn-login">
      Log In
    </button>
  </div>
</template>

<style scoped>
.auth-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 1.5rem 0;
}

.btn-login {
  display: inline-block;
  background-color: #1f1841;
  color: #ffffff;
  font-weight: 600;
  font-size: 0.95rem;
  padding: 8px 18px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  cursor: pointer;
}

.btn-login:hover {
  border-color: #81d4fa;
  color: #81d4fa;
}
</style>
