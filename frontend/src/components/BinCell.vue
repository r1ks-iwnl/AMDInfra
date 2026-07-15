<script setup>
defineProps({ bin: {type: Object, required: true}})
</script>

<template>
  <div class="bin-cell" :class="bin.hit ? 'hit' : 'miss'" :title="`${bin.name} - hits=${bin.hits}`">
    <span>{{ bin.value || bin.name }}</span>
    <span>{{ bin.hit ? 'HIT' : 'MISS' }} - {{ bin.hits }}</span>
  </div>
</template>

<style scoped>
.bin-cell {
  padding: 10px;
  border-radius: 6px;
  color: #ffffff;
  text-align: center;
  display: flex;
  flex-direction: column;
  font-size: 0.9rem;
  font-weight: 600;
}
.hit { background-color: var(--color-success); }
.miss { background-color: var(--color-bad); }
</style>
