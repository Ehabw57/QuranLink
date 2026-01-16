<template>
  <template v-for="(word, index) in verse.simple_text" :key="index">
    <TextInput
      v-if="index === activeIndex"
      ref="inputs"
      @correct="handleCorrect"
      :expected="currentExpected"
    />

    <p class='dashes' v-else-if="index > activeIndex && inputIndexs.includes(index)">
      {{ generateDashes(word.length) }}
    </p>
    <p 
      ref='words' 
      :class="{ correct: oldInputIndexs.includes(index) }" 
      class="quran-text" 
      v-else
    > 
      {{ verse.text[index] }} 
    </p>
  </template>

  <p class="quran-text">{{ verse.glyph_number }}</p>
</template>

<script>
import { ref, computed, nextTick } from 'vue';
import { store } from '@/store';
import { shuffleArray, delay, generateDashes } from '@/utils/helpers';
import TextInput from '@/components/ui/TextInput.vue';

export default {
  name: 'WordTest',
  components: { TextInput },
  props: {
    verse: { type: Object, required: true },
  },
  emits: ['done'],
  setup(props, { emit, expose }) {
    const inputs = ref([]);
    const words = ref([]);
    const activeIndex = ref(0);
    const oldInputIndexs = ref([]);
    const inputIndexs = ref([]);
    
    const currentExpected = computed(() => {
      return props.verse.simple_text[activeIndex.value] || '';
    });
    
    const handleCorrect = async () => {
      if (inputIndexs.value.length <= 1) {
        emit('done');
        return;
      }
      inputIndexs.value.shift();
      activeIndex.value = inputIndexs.value[0];
      await focusInput();
      const word = words.value[words.value.length - 1];
      await delay(600);
      word.classList.remove('correct');
    };
    
    const pickInputIndexs = () => {
      inputIndexs.value = [0];
      const verseLength = props.verse.text.length;
      if (verseLength > 1) {
        const inputsCount = Math.floor(verseLength * 0.5);
        let map = Array.from({ length: verseLength }, (_, i) => i);
        inputIndexs.value = shuffleArray(map)
          .slice(0, inputsCount)
          .sort((a, b) => a - b);
      }
      activeIndex.value = inputIndexs.value[0];
    };
    
    const focusInput = async () => {
      await nextTick();
      if (inputs.value?.length > 0) {
        const input = inputs.value[0];
        store.setCurrentInput(input);
        input.focus();
      }
    };
    
    const restartTest = () => {
      pickInputIndexs();
      oldInputIndexs.value = [...inputIndexs.value];
      focusInput();
    };
    
    expose({ restartTest });
    
    return {
      inputs,
      words,
      activeIndex,
      oldInputIndexs,
      inputIndexs,
      currentExpected,
      handleCorrect,
      restartTest,
      generateDashes,
    };
  },
};
</script>
