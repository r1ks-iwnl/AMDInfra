<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { useRunDetailStore } from '@/stores/rundetail'
import { fmtDate, fmtPct, covClass } from '@/utils/format'

const store = useRunDetailStore()
const route = useRoute()

watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      store.fetchRunDetail(newId)
    }
  },
  { immediate: true }
)
</script>


<template><!-- nesting nightmare, change entirely or perhaps some grouping via styling is enough to make it more readable. -->
  <p v-if="store.loading">Loading...</p>
  <p v-else-if="store.error">{{ store.error }}</p>
  <ul v-else-if="store.currentRun">
      <li>ID: {{ store.currentRun.id }}</li>
      <li>File name: {{ store.currentRun.filename }}</li>
      <li>Run date: {{ fmtDate(store.currentRun.run_date) }}</li>
      <li>Result: {{ store.currentRun.result }}</li>
      <li>Overall coverage: {{ fmtPct(store.currentRun.overall_coverage) }}</li>
      <li>Checks: {{ store.currentRun.checks }}</li>
      <li>Uploaded at: {{ fmtDate(store.currentRun.uploaded_at) }}</li>
      <li>Uploaded by: {{ store.currentRun.uploaded_by }}</li>
      <li>Total bins: {{ store.currentRun.total_bins }}</li>
      <li>Missed bins: {{ store.currentRun.miss_bins }}</li>

      <details><summary>Coverpoints:</summary>
        <ul v-for="cp in store.currentRun.coverpoints" :key="cp.id">
          <details><summary>{{ cp.name }}</summary>
            <li>Coverage: {{ fmtPct(cp.coverage) }}</li>
            <li>Total bins: {{ cp.total_bins }}</li>
            <li>Missed bins: {{ cp.missed_bins }}</li>

            <details><summary>Bins:</summary>
              <ul v-for="bin in cp.bins" :key="bin.id">
                <details><summary>{{ bin.name }}</summary>
                  <li>Value: {{ bin.value }}</li>
                  <li>Hits: {{ bin.hits }}</li>
                  <li>Hit: {{ bin.hit }}</li>
                </details>
              </ul>
            </details>
          </details>
        </ul>
      </details>

  </ul>
</template>
