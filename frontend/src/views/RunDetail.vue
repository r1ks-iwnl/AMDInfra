<script setup>
import { computed, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useRunDetailStore } from '@/stores/rundetail'
import { covClass, fmtDate, fmtPct } from '@/utils/format'

import BinCell from '@/components/BinCell.vue'
import CoverageBar from '@/components/CoverageBar.vue'

import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend as ChartLegend, BarElement, CategoryScale, LinearScale } from 'chart.js'
ChartJS.register(Title, Tooltip, ChartLegend, BarElement, CategoryScale, LinearScale)

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

const colorMap = {
  'cov-good': '#2ecc71',
  'cov-warn': '#f39c12',
  'cov-bad': '#e74c3c'
}

const chartData = computed(() => {
  if (!store.currentRun || !store.currentRun.coverpoints) return null

  const barColor = colorMap[covClass(store.currentRun.overall_coverage)]

  return {
    labels: store.currentRun.coverpoints.map(cp => cp.name),
    datasets: [{
      label: 'Coverage (%)',
      backgroundColor: (barColor || '#81d4fa'),
      data: store.currentRun.coverpoints.map(cp => cp.coverage)
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: { beginAtZero: true, max: 100, ticks: { color: '#bfafe3' },
      grid: {
            color: 'rgba(255, 255, 255, 0.15)',
            borderColor: 'rgba(255, 255, 255, 0.3)'
          } },
    x: { ticks: { color: '#bfafe3' },
      grid: {
            color: 'rgba(255, 255, 255, 0.15)',
            borderColor: 'rgba(255, 255, 255, 0.3)'
          } }
  },
  plugins: { legend: { labels: { color: '#ffffff' } } }
}
</script>

<template>
  <div class="run-detail-wrapper">
    <div v-if="store.loading" class="state-box">Loading run details...</div>

    <div v-else-if="store.error" class="state-box error-404">
      <p>{{ store.error }}</p>
    </div>

    <div v-else-if="store.currentRun" class="dashboard">

      <section class="header-card">
        <h1>{{ store.currentRun.filename }}</h1>
        <div class="meta-grid">
          <div><strong>Ran at:</strong> {{ fmtDate(store.currentRun.run_date) }}</div>
          <div><strong>Uploaded at:</strong> {{ fmtDate(store.currentRun.uploaded_at) }}</div>
          <div><strong>Uploaded by:</strong> {{ store.currentRun.uploaded_by }}</div>
          <div>
            <strong>Result:</strong>
            <span class="badge" :class="store.currentRun.result.toLowerCase()">{{ store.currentRun.result }}</span>
          </div>
          <div><strong>Bins (missed / total):</strong> {{ store.currentRun.missed_bins }} / {{ store.currentRun.total_bins }}</div>
        </div>

        <div class="overall-section">
          <CoverageBar
            label="Overall coverage"
            :percent="store.currentRun.overall_coverage"
          />
        </div>
      </section>

      <section class="chart-section" v-if="chartData">
        <div class="chart-container">
          <Bar :data="chartData" :options="chartOptions" />
        </div>
      </section>

      <section class="legend">
        <strong>Bin legend:</strong>
        <span class="legend-item"><span class="color-box hit"></span>HIT</span>
        <span class="legend-item"><span class="color-box miss"></span>MISS</span>
      </section>

      <section class="coverpoints-container">
        <div
          v-for="cp in store.currentRun.coverpoints"
          :key="cp.id"
          class="cp-card"
          :class="`${covClass(cp.coverage)}-border`">

          <div class="cp-header">
            <CoverageBar :label="cp.name" :percent="cp.coverage" />
            <div class="cp-summary">
              {{ cp.total_bins - cp.missed_bins }} / {{ cp.total_bins }} bins covered
            </div>
          </div>

          <div
            class="bin-grid"
            :class="cp.name === 'cp_vec' ? 'grid-4x4' : 'grid-auto'">

            <BinCell v-for="b in cp.bins" :key="b.id" :bin="b" />
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<style scoped>
.run-detail-wrapper {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}
.top-nav { margin-bottom: 20px; }
.back-link {
  color: #81d4fa;
  text-decoration: none;
  font-weight: 600;
}
.back-link:hover { text-decoration: underline; }

.state-box {
  text-align: center;
  padding: 60px 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: #bfafe3;
}
.error-404 h2 { color: #e74c3c; margin-bottom: 10px; }
.btn-primary {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background: #1f1841;
  color: #ffffff;
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 6px;
  text-decoration: none;
}

.header-card {
  background: rgba(255, 255, 255, 0.03);
  padding: 24px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: 30px;
}
.header-card h1 { margin: 0 0 16px 0; font-size: 1.8rem; }
.meta-grid {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
  margin-bottom: 24px;
  color: #e2def5;
}
.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}
.badge.passed { background: rgba(46, 204, 113, 0.15); color: #d4edda; }
.badge.failed { background: rgba(231, 76, 60, 0.15); color: #f8d7da; }

.chart-section {
  background: rgba(255, 255, 255, 0.02);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 30px;
}
.chart-container { height: 250px; }

.legend {
  display: flex;
  gap: 20px;
  align-items: center;
  margin-bottom: 20px;
  padding: 12px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}
.color-box {
  display: inline-block;
  width: 16px;
  height: 16px;
  border-radius: 4px;
  vertical-align: middle;
  margin-right: 5px;
}
.color-box.hit { background-color: #2ecc71; }
.color-box.miss { background-color: #e74c3c; }

.cp-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}
.cp-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px dashed rgba(255,255,255,0.1);
}
.cp-summary {
  text-align: right;
  font-size: 0.9rem;
  color: #bfafe3;
  margin-top: 8px;
}

.cov-good {
  background-color: #2ecc71 !important;
  color: #2ecc71 !important;
}
.cov-warn {
  background-color: #f39c12 !important;
  color: #f39c12 !important;
}
.cov-bad {
  background-color: #e74c3c !important;
  color: #e74c3c !important;
}

.cov-good-border {
  border-color: #2ecc71;
}
.cov-warn-border {
  border-color: #f39c12;
}
.cov-bad-border {
  border-color: #e74c3c;
}

.bin-grid {
  display: grid;
  gap: 10px;
}
.grid-auto {
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
}
.grid-4x4 {
  grid-template-columns: repeat(4, 1fr);
}

@media (max-width: 768px) {
  .grid-4x4 { grid-template-columns: repeat(2, 1fr); }
  .meta-grid { flex-direction: column; gap: 10px; }
}
</style>
