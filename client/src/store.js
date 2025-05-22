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


  delay(ms) {
    return new Promise(reslove => setTimeout(reslove, ms))
  },

  generateDashes(length) {
    return '_'.repeat(length);
  },
})
