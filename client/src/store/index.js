import { reactive } from 'vue';

export const store = reactive({
  currentInput: null,

  setCurrentInput(ref) {
    this.currentInput = ref;
  },
});
