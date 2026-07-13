import { defineStore } from 'pinia'
import api from '@/api/client'

export const useRunDetailStore = defineStore('runDetail', {
  state: () => ({
    currentRun: null,
    loading: false,
    error: null
  }),

  actions: {
    async fetchRunDetail(runId) {
      this.loading = true
      this.error = null
      this.currentRun = null

      try {
        const { data } = await api.get(`/runs/${runId}`)
        this.currentRun = data
      } catch (e) {
        this.error = e.response?.data?.detail || "Couldn't load run details."
      } finally {
        this.loading = false
      }
    }
  }
})
