<script setup>
import { ref } from 'vue'
import { RouterLink , RouterView } from 'vue-router'
import RunsList from './views/RunsList.vue';
import LoginView from './views/LoginView.vue';

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
