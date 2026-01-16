<template>
  <p class="quran-text" v-for="(word, index) in verses[0].text" :key="index">{{ word }}</p>
  <p class="quran-text">{{ verses[0].glyph_number }}</p>

  <div class="verseBlock" v-if="verses[1]">
    <template v-for="(word, index) in verses[1].text" :key="index">
      <TextInput
        v-if="activeIndex === index"
        ref="inputs"
        :expected="currentExpected"
        @correct="handleCorrect()"
      />

      <p class="correct quran-text" v-else-if="activeIndex > index" ref="words">
        {{ word }}
      </p>
      <p class="dashes" v-else>
        {{ generateDashes(verses[1].simple_text[index].length) }}
      </p>
    </template>

    <p class="quran-text">{{ verses[1].glyph_number }}</p>
  </div>
</template>

<script>
import { ref, computed, nextTick } from 'vue';
import { store } from '@/store';
import { delay, generateDashes } from '@/utils/helpers';
import TextInput from '@/components/ui/TextInput.vue';

export default {
  name: 'VerseTest',
  components: { TextInput },
  props: {
    verses: { type: Array, required: true },
  },
  emits: ['done'],
  setup(props, { emit, expose }) {
    const inputs = ref([]);
    const words = ref([]);
    const activeIndex = ref(0);
    
    const currentExpected = computed(() => {
      return props.verses[1]?.simple_text[activeIndex.value] || '';
    });
    
    const handleCorrect = async () => {
      const questionVerse = props.verses[1];
      if (activeIndex.value === questionVerse.text.length - 1) {
        emit('done');
      } else {
        activeIndex.value++;
        await focusInput();
        const word = words.value[activeIndex.value - 1];
        await delay(600);
        word.classList.remove('correct');
      }
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
      activeIndex.value = 0;
      focusInput();
    };
    
    expose({ restartTest });
    
    return {
      inputs,
      words,
      activeIndex,
      currentExpected,
      handleCorrect,
      restartTest,
      generateDashes,
    };
  },
};
</script>
