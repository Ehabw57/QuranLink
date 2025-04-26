<template>
  <div v-for="(word, index) in verse.simple_text" :key="index">
    <inputBox
    v-if="isCurrentInput(index)"
    ref="input"
    @correct="handleCorrect(index)"
    :expected="word"
    />

    <p :class="{ correct: correctStates[index] }" class="quran-text" v-else-if="isDisplayed(index)">
    {{ verse.text[index] }}
    </p>

    <p class='dashes' v-else>{{ store.generateDashes(word.length) }}</p>
  </div>

  <p class="quran-text">{{ verse.glyph_number }}</p>
</template>

<script>
  import { store } from '../store.js';

  export default {
    props: {
      verse: { type: Object, required: true },
      modelValue: { type: Number, required: true }
  },
  emits: ['done', 'update:modelValue'],
  data() {
    return {
      store,
      currentInput: 0,
      activeIndex: 0,
      arrayMap: [],
      correctWords: {},
      correctStates: {}
    };
  },
  methods: {
    focusInput() {
      this.$nextTick(() => {
        const nextInput = this.$refs.input?.[0];
        if (nextInput) {
          this.store.setCurrentInput(nextInput);
          nextInput.focus();
        }
      });
    },
    isCurrentInput(index) {
      return this.arrayMap.includes(index) && this.currentInput === index;
    },
    isDisplayed(index) {
      return !this.arrayMap.includes(index) || this.correctWords[index];
    },
    handleCorrect(index) {
      this.correctWords[index] = true;
      this.correctStates[index] = true;

      setTimeout(() => {
        this.correctStates[index] = false;
      }, 500);

      this.activeIndex++;
      this.currentInput = this.arrayMap[this.activeIndex];

      if (this.currentInput !== undefined) {
        this.focusInput();
      } else {
        this.$emit('done');
      }
    },
    createMap() {
      const verseLength = this.verse.text.length;
      this.arrayMap = [0];
      this.currentInput = 0;

      if (verseLength > 1) {
        const arrayLength = Math.floor(verseLength * 0.5);
        let map = Array.from({ length: verseLength }, (_, i) => i);
        this.arrayMap = this.store
          .shuffleArray(map)
          .slice(0, arrayLength)
          .sort((a, b) => a - b);
        this.currentInput = this.arrayMap[0];
      }

      this.$emit('update:modelValue', this.verse.surah_id);
    },
    restartTest() {
      this.activeIndex = 0;
      this.currentInput = 0;
      this.correctWords = {};
      this.correctStates = {};
      this.createMap();
      this.focusInput();
    }
  },
  watch: {
    verse: {
      handler() {
        this.restartTest();
      },
      deep: true,
      immediate: true
    }
  }
};
</script>

