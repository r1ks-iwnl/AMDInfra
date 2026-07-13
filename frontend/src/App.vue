<script setup>
import { ref } from 'vue'
import { RouterLink , RouterView } from 'vue-router'

const isLoggedIn = ref(false)

function onLoginDone() {
  isLoggedIn.value = true
}
</script>

<template>
  <nav class="app-nav">
    <RouterLink to="/runs">Runs</RouterLink>
  </nav>
  <RouterView/>
</template>

<style scoped>
</style>
