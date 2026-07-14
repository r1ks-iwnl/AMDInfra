<script setup>
import { computed } from 'vue'
import { fmtPct, covClass } from '@/utils/format'

const props = defineProps({
  label: { type: String, required: true },
  percent: { type: [Number, String], required: true}
})

const pct = computed(() => Number(props.percent))

const color = computed(() => covClass(pct.value))

const width = computed(() => `${Math.min(100, Math.max(0, pct.value))}%`)
</script>

<template>
  <div class="cov-bar">
    <div class="cov-head">
      <span>{{ label }}</span>
      <span>{{ fmtPct(pct) }}</span>
    </div>
    <div class="track">
      <div class="fill" :class="color" :style="{ width: width}"></div>
    </div>
  </div>
</template>

<style scoped>
.cov-bar {
  width: 100%;
}
.cov-head {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  font-weight: bold;
}
.track {
  width: 100%;
  height: 12px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  overflow: hidden;
}
.fill {
  height: 100%;
  border-radius: 6px;
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
</style>
