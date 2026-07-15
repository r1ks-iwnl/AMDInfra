import { defineStore } from 'pinia'
import { getRunDetail } from '@/api/runs'

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
        this.currentRun = await getRunDetail(runId)
      } catch (e) {
        if (e.response?.status === 404) {
          this.error = "Run not found."
        } else {
        this.error = e.response?.data?.detail || "Couldn't load run details."
        }
      } finally {
        this.loading = false
      }
    }
  }
})
