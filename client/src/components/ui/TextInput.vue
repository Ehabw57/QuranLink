<template>
  <span class="text-input-wrapper">
    <span class="length-indicator">
      <span>{{ expected.length }}</span>
      <span>{{ lengthLabel }}</span>
    </span>
    <textarea ref="inputRef" rows="1" tabindex="1" class="text-input input" :class="{ shake: isShaking }"
      v-model="inputValue" @input="handleInput" :style="{ width: inputWidth }"></textarea>
  </span>
</template>

<script>
import { ref, computed } from 'vue';
import { simplifyArabicText } from '@/utils/textUtils';

export default {
  name: 'TextInput',
  props: {
    expected: { type: String, required: true },
    lengthLabel: { type: String, default: '' },
  },
  emits: ['correct'],
  setup(props, { emit, expose }) {
    const inputRef = ref(null);
    const inputValue = ref('');
    const hint = ref('');
    const isShaking = ref(false);

    const inputWidth = computed(() => `${props.expected.length + 2}ch`);

    const emitCorrect = () => {
      emit('correct');
      inputValue.value = '';
      hint.value = '';
    };

    const addHint = () => {
      if (hint.value.length < props.expected.length - 1) {
        hint.value += props.expected[hint.value.length];
        inputValue.value = hint.value;
      } else {
        emitCorrect();
      }
    };

    const handleInput = () => {
      const lastChar = inputValue.value[inputValue.value.length - 1];

      if (lastChar === ' ') {
        addHint();
        return;
      }

      if (lastChar === '\n') {
        emitCorrect();
        return;
      }

      if (inputValue.value.length === props.expected.length) {
        if (simplifyArabicText(inputValue.value) === simplifyArabicText(props.expected)) {
          emitCorrect();
        } else {
          isShaking.value = true;
          setTimeout(() => {
            inputValue.value = hint.value;
            isShaking.value = false;
          }, 400);
        }
      }
    };

    const focus = () => inputRef.value?.focus();
    const reset = () => {
      inputValue.value = '';
      hint.value = '';
    };

    expose({ focus, reset });

    return {
      inputRef,
      inputValue,
      isShaking,
      inputWidth,
      handleInput,
    };
  },
};
</script>

<style scoped>
  .text-input-wrapper {
    display: inline-block;
  }

  .length-indicator { 
    display: flex; 
    justify-content: center; 
    margin-bottom: 5px;
    flex-direction: row-reverse;
    gap: 3px; 
    font-size: 0.7rem; 
    color: var(--color-muted);
  }

  html[dir="rtl"] .length-indicator {
    flex-direction: row;
  }

</style>