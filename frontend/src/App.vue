<script setup>
import { RouterLink , RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth';
import router  from '@/router';

const auth = useAuthStore()

function handleLogout() {
  auth.logout()
  router.push('/login')
}

</script>

<template>
  <nav class="app-nav">
    <div class="nav-left"></div>

    <div class="nav-center">
      <RouterLink class="btn" to="/runs">Runs</RouterLink>
      <RouterLink class="btn" to="/upload">Upload</RouterLink>
    </div>

    <div class="nav-right">
      <div v-if="auth.isLoggedIn && auth.user" class="user-profile">
        <span class="email">{{ auth.user.email }}</span>
        <button @click="handleLogout()" class="btn btn-logout">Logout</button>
      </div>
    </div>
  </nav>

  <RouterView/>
</template>

<style scoped>
.app-nav {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  margin: 2rem 0;
  width: 100%;
  box-sizing: border-box;
}

.nav-left {
  flex: 1;
}

.nav-center {
  display: flex;
  gap: 1rem;
}

.nav-right {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.email {
  color: var(--color-text-muted, #bfafe3);
  font-size: 0.9rem;
  font-weight: 500;
}

.btn {
  display: inline-block;
  background-color: var(--color-bg-dark);
  color: #ffffff;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  padding: 10px 24px;
  border-radius: 8px;
  border: 1px solid var(--color-grid-line);
  cursor: pointer;
  font-family: inherit;
}

.btn:hover {
  background-color: rgba(255, 255, 255, 0.08);
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.btn:active {
  transform: translateY(1px);
}

.router-link-active.btn {
  border-color: var(--color-accent);
  color: var(--color-accent);
  background-color: var(--color-accent-transparent);
}

.btn-logout {
  padding: 8px 16px;
  font-size: 0.9rem;
}
</style>
