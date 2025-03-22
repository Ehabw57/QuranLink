import { reactive } from "vue";

export const store = reactive({
  currentInputIndex: 0,
  incrementIndex () {
    this.currentInputIndex++
  },
  resetIndex () {
    this.currentInputIndex = 0
  }
})
