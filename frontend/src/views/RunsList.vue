<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRunsStore } from '@/stores/runs'
import { fmtDate, fmtPct, covClass } from '@/utils/format'
import { getSortIcon } from '@/utils/icons'

const store = useRunsStore()
const router = useRouter()

onMounted(async () => {
  // Maintain sort state
  if (store.runs.length === 0) {
    await store.fetchRuns()
  }
})
</script>

<template>
  <div class="runs-wrapper">
    <p v-if="store.loading" class="loading-state">Loading runs...</p>
    <p v-else-if="store.error" class="error-state">{{ store.error }}</p>
    <p v-else-if="!store.sortedRuns || store.sortedRuns.length === 0" class="empty-state">
      Runs have not yet been uploaded.
    </p>

    <div v-else>
      <div class="summary-bar">
        <div class="summary-item">
          <span class="summary-label">Total Runs</span>
          <span class="summary-value">{{ store.totalRuns }}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Average Coverage</span>
          <span class="summary-value" :class="covClass(store.avgCoverage)">
            {{ fmtPct(store.avgCoverage) }}
          </span>
        </div>
      </div>
      <table class="runs-table">
        <thead>
          <tr>
            <th @click="store.changeSort('run_date')" class="sortable-th">
              Date {{ getSortIcon('run_date', store.sortBy, store.sortDesc) }}
            </th>
            <th @click="store.changeSort('filename')" class="sortable-th">
              File {{ getSortIcon('filename', store.sortBy, store.sortDesc) }}
            </th>
            <th @click="store.changeSort('overall_coverage')" class="sortable-th">
              Overall coverage {{ getSortIcon('overall_coverage', store.sortBy, store.sortDesc) }}
            </th>
            <th @click="store.changeSort('result')" class="sortable-th">
              Result {{ getSortIcon('result', store.sortBy, store.sortDesc) }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="run in store.sortedRuns" :key="run.id"
            @click="router.push(`/runs/${run.id}`)" class="run-row"
            @keydown.enter="router.push(`/runs/${run.id}`)"
            @keydown.space.prevent="router.push(`/runs/${run.id}`)"
            tabindex="0">
            <td>{{ fmtDate(run.run_date) }}</td>
            <td>
              {{ run.filename }}
            </td>
            <td :class="covClass(run.overall_coverage)">
              {{ fmtPct(run.overall_coverage) }}
            </td>
            <td>
              <span class="badge" :class="run.result.toLowerCase()">
                {{ run.result }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.sortable-th {
  cursor: pointer;
}

.sortable-th:hover {
  background-color: rgba(255, 255, 255, 0.08);
}

.runs-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th, td {
  padding: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  text-align: left;
}

th {
  background-color: var(--color-bg-dark);
  font-weight: 600;
  border-bottom: 2px solid var(--color-grid-line);
}

.run-link {
  color: var(--color-accent) !important;
  font-weight: 500;
  text-decoration: underline;
}
.run-link:hover {
  color: var(--color-accent-hover) !important;
}

.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 40px;
  color: var(--color-text-secondary) !important;
  font-size: 1.1rem;
}
.run-row {
  cursor: pointer;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
  font-size: 0.85rem;
  text-transform: uppercase;
}
.badge.passed {
  background-color: var(--color-badge-passed-bg);
  color: var(--color-success);
  border: 1px solid var(--color-success);
}
.badge.failed {
  background-color: var(--color-badge-failed-bg);
  color: var(--color-bad);
  border: 1px solid var(--color-bad);
}

.cov-good {
  color: var(--color-success) !important;
  font-weight: bold;
}
.cov-warn {
  color: var(--color-warning) !important;
  font-weight: bold;
}
.cov-bad {
  color: var(--color-bad) !important;
  font-weight: bold;
}

.summary-bar {
  display: flex;
  gap: 20px;
  margin-bottom: 1.5rem;
  justify-content: center;
}

.summary-item {
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 12px 20px;
  border-radius: 8px;
  min-width: 150px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.summary-label {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.summary-value {
  font-size: 1.6rem;
  font-weight: bold;
}
</style>
