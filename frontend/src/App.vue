<script setup>
import { ref } from 'vue'
import RunsList from './views/RunsList.vue';
import LoginView from './views/LoginView.vue';

const isLoggedIn = ref(!!localStorage.getItem('access_token'))

function onLoginDone() {
  isLoggedIn.value = true
}

</script>

<template>
  <LoginView v-if="!isLoggedIn" @auth-success="onLoginDone" />
  <RunsList v-else />
</template>

<style scoped>
</style>
