<script setup>
import { ref } from 'vue'
import api, { getLoginUrl } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const loginUrl = getLoginUrl

function handleLogin() {
  const width = 500, height = 600
  const left = window.screen.width / 2 - width / 2
  const top = window.screen.height / 2 - height / 2

  const popup = window.open(
    loginUrl,
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
    <button v-if="!isAuthenticated" @click="handleLogin" class="btn-login">
      Log In
    </button>
  </div>
</template>
