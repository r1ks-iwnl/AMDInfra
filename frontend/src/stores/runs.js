import { defineStore } from 'pinia'
import { getRuns } from '@/api/runs'
import api from '@/api/client'

export const useRunsStore = defineStore('runs', {
  state: () => ({
    runs: [],
    loading: false,
    error: null,

    sortBy: 'run_date',
    sortDesc: true
  }),

  getters: {
    // sorting is a logical task and as such is kept closer to the data origin as opposed to doing it in the component.
    sortedRuns: (state) => {
      if (!state.runs) return []

      return [...state.runs].sort((a, b) => {
        let modifier = state.sortDesc ? -1 : 1

        let valA = a[state.sortBy]
        let valB = b[state.sortBy]

        // filename sorting
        if (typeof valA === 'string' && typeof valB === 'string') {
          return valA.localeCompare(valB) * modifier
        }

        // number/date sorting
        if (valA < valB) return -1 * modifier
        if (valA > valB) return 1 * modifier
        return 0
      })
    },
    totalRuns: (state) => state.runs.length,
    avgCoverage: (state) =>
      state.runs.length
        ? state.runs.reduce((s, r) => s + r.overall_coverage, 0) /
          state.runs.length
        : 0,
  },

  actions: {
    async fetchRuns() {
      this.loading = true
      this.error = null
      try {
        this.runs = await getRuns()
      } catch (e) {
        this.error = e.response?.data?.detail || "Couldn't load runs."
      } finally {
        this.loading = false
      }
    },

    changeSort(column) {
      // reverse sorting order when clicking column
      if (this.sortBy === column) {
        this.sortDesc = !this.sortDesc
      } else {
        // activate sorting on a different column
        this.sortBy = column
        this.sortDesc = true
      }
    }
  }
})
