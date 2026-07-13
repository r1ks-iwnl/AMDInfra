<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useRunsStore } from '@/stores/runs'
import { fmtDate, fmtPct, covClass } from '@/utils/format'
import { getSortIcon } from '@/utils/icons'

const store = useRunsStore()

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
      No runs uploaded.
    </p>

    <table v-else class="runs-table">
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
        <tr v-for="run in store.sortedRuns" :key="run.id">
          <td>{{ fmtDate(run.run_date) }}</td>
          <td>
            <RouterLink :to="`/runs/${run.id}`" class="run-link">
              {{ run.filename }}
            </RouterLink>
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
</template>

<style scoped>
.sortable-th {
  cursor: pointer;
}

.runs-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th, td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}
th {
  background-color: #f4f6f7;
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
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}
.badge.failed {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.cov-good {
  color: #2ecc71 !important;
  font-weight: bold;
}
.cov-warn {
  color: #f39c12 !important;
  font-weight: bold;
}
.cov-bad {
  color: #e74c3c !important;
  font-weight: bold;
}
</style>
