import { reactive } from "vue";

export const store = reactive({
  currentInput: null,

  setCurrentInput(ref) {
    this.currentInput = ref
  },

  shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[j], array[i]] = [array[i], array[j]];
    }
    return array;
  },

  chunkArray(array, size) {
    const chunks = [];
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size));
    }
    return chunks;
  },

  generateDashes(length) {
    return '_'.repeat(length);
  },
})
