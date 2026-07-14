<script setup>
import { RouterLink , RouterView } from 'vue-router'
</script>

<template>
  <nav class="app-nav">
    <RouterLink class="runs-btn" to="/runs">Runs</RouterLink>
  </nav>
  <RouterView/>
</template>

<style scoped>
.app-nav {
  display: flex;
  justify-content: center;
  margin: 2rem 0;
  width: 100%;
}

.runs-btn {
  display: inline-block;
  background-color: #1f1841;
  color: #ffffff;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  padding: 10px 24px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  cursor: pointer;
}

.runs-btn:hover {
  background-color: rgba(255, 255, 255, 0.08);
  border-color: #81d4fa;
  color: #81d4fa;
}

.runs-btn:active {
  transform: translateY(1px);
}

.router-link-active.runs-btn {
  border-color: #81d4fa;
  color: #81d4fa;
  background-color: rgba(129, 212, 250, 0.1);
}
</style>
