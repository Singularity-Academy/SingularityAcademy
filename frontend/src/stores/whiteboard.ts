import { defineStore } from 'pinia'

export interface TimelineNode {
  id: string
  title: string
  description: string
  components: any[]
}

export const useWhiteboardStore = defineStore('whiteboard', {
  state: () => ({
    timeline: [] as TimelineNode[],
    currentNodeIndex: 0,
    pages: [[]] as any[][],
  }),
  actions: {
    setTimeline(timeline: TimelineNode[]) {
      this.timeline = timeline
      this.currentNodeIndex = 0
    },
    nextNode() {
      if (this.currentNodeIndex < this.timeline.length - 1) {
        this.currentNodeIndex++
      }
    },
    prevNode() {
      if (this.currentNodeIndex > 0) {
        this.currentNodeIndex--
      }
    },
    addComponentToCurrentPage(component: any) {
      this.pages[this.currentNodeIndex].push(component)
    }
  }
})