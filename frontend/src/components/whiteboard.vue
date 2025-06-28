<template>
  <div class="whiteboard">
    <ToolBar @addComponent="addComponent" />
    <div class="board-area">
      <component
        v-for="(comp, idx) in currentPage"
        :is="comp.type"
        v-bind="comp.props"
        :key="idx"
      />
    </div>
    <Timeline
      :timeline="timeline"
      :current="currentNodeIndex"
      @select="selectNode"
      @next="nextNode"
      @prev="prevNode"
    />
  </div>
</template>

<script setup lang="ts">

import { computed } from 'vue'
import { useWhiteboardStore } from '@/stores/whiteboard'
import ToolBar from '@/components/toolbar.vue'
import Timeline from '@/components/timeline.vue'

const whiteboard = useWhiteboardStore()
const timeline = computed(() => whiteboard.timeline)
const currentNodeIndex = computed(() => whiteboard.currentNodeIndex)
const currentPage = computed(() => whiteboard.pages[currentNodeIndex.value] || [])

function addComponent(component: any) {
  whiteboard.addComponentToCurrentPage(component)
}
function selectNode(index: number) {
  whiteboard.currentNodeIndex = index
}
function nextNode() {
  whiteboard.nextNode()
}
function prevNode() {
  whiteboard.prevNode()
}
</script>

<style scoped>
.whiteboard {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.board-area {
  flex: 1;
  background: #fff;
  border: 1px solid #eee;
  margin: 1rem 0;
  min-height: 400px;
  position: relative;
}
</style>