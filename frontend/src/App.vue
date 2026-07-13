<script setup>
import { RouterLink , RouterView } from 'vue-router'
</script>

<template>
  <nav class="app-nav">
    <RouterLink to="/runs">Runs</RouterLink>
  </nav>
  <RouterView/>
</template>

<style scoped>
</style>
