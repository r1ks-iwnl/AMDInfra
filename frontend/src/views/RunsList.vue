<script setup>
import { ref, onMounted } from 'vue'
import api from '../api/client'

const runs = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await api.get('/runs/')
    runs.value = res.data
  } catch (e) {
    error.value = "We couldn't load runs."
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <p v-if="loading">Loading...</p>
  <p v-else-if="error">{{ error }}</p>
  <ul v-else>
    <li v-for="r in runs" :key="r.id">{{ r.filename }} - {{ r.overall_coverage }}%</li>
  </ul>
</template>
