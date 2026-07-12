<script setup>
import { ref } from 'vue'

const isAuthenticated = ref(!!localStorage.getItem('access_token'))

const emit = defineEmits(['auth-success'])

function handleLogin() {
  const width = 500, height = 600
  const left = window.screen.width / 2 - width / 2
  const top = window.screen.height / 2 - height / 2

  const popup = window.open(
    'http://localhost:8000/auth/login',
    'Google Login',
    `width=${width},height=${height},left=${left},top=${top}`
  )

  window.addEventListener('message', (event) => {
    if (event.origin !== 'http://localhost:8000') return

    if (event.data && event.data.token) {
      localStorage.setItem('access_token', event.data.token)
      isAuthenticated.value = true
      popup.close()
      emit('auth-success')
    }
  }, { once: true })
}
</script>

<template>
  <div class="auth-bar">
    <button v-if="!isAuthenticated" @click="handleLogin" class="btn login">
      Log In
    </button>
  </div>
</template>
