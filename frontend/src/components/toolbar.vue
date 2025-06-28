<template>
  <div class="toolbar">
    <button @click="add('math')">数学组件</button>
    <button @click="add('physics')">物理组件</button>
    <button @click="add('text')">文本组件</button>
  </div>
</template>
<script setup lang="ts">
const emit = defineEmits(['addComponent'])
function add(type: string) {
  emit('addComponent', { type, props: {} })
}
</script>
<style scoped>
.toolbar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}
</style>