<template>
  <div class="timeline">
    <button @click="$emit('prev')" :disabled="current === 0">上一节点</button>
    <span v-for="(node, idx) in timeline" :key="node.id"
      :class="{ active: idx === current }"
      @click="$emit('select', idx)">
      {{ node.title }}
    </span>
    <button @click="$emit('next')" :disabled="current === timeline.length - 1">下一节点</button>
  </div>
</template>
<script setup lang="ts">
defineProps<{
  timeline: any[]
  current: number
}>()
</script>
<style scoped>
.timeline {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.active {
  font-weight: bold;
  color: #409eff;
}
</style>