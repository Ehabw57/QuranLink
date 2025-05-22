<template>
  <div v-for="(word, index) in verse.simple_text" :key="index">
    <inputBox
    v-if="index === activeIndex"
    ref="inputs"
    @correct="handleCorrect"
    :expected="word"
    />

    <p class='dashes' v-else-if="index > activeIndex && inputIndexs.includes(index)">{{ store.generateDashes(word.length) }}</p>
    <p ref='words' :class="{correct: oldInputIndexs.includes(index)}" class="quran-text" v-else> {{ verse.text[index] }} </p>
  </div>

  <p class="quran-text">{{ verse.glyph_number }}</p>
</template>

<script>
  import { store } from '../store.js';

  export default {
    props: {
      verse: { type: Object, required: true },
    },
    emits: ['done'],
    data() {
      return {
        store,
        activeIndex: 0,
        oldInputIndexs:[],
        inputIndexs: [],
      };
    },
    methods: {
      async handleCorrect() {
        if(this.inputIndexs.length <= 1) {
          this.$emit('done');
          return;
        }
        this.inputIndexs.shift();
        this.activeIndex = this.inputIndexs[0];
        await this.focusInput();
        const word = this.$refs.words[this.$refs.words.length - 1]
        await this.store.delay(600);
        word.classList.remove('correct');
      },

      pickInputIndexs() {
        this.inputIndexs = [0];
        const verseLength = this.verse.text.length;
        if (verseLength > 1) {
          const inputsCount = Math.floor(verseLength * 0.5);
          let map = Array.from({ length: verseLength }, (_, i) => i);
          this.inputIndexs = this.store
            .shuffleArray(map)
            .slice(0, inputsCount)
            .sort((a, b) => a - b);
        }
        this.activeIndex = this.inputIndexs[0];
      },

      async focusInput() {
        await this.$nextTick();
        if (this.$refs.inputs?.length > 0 ) {
          const input = this.$refs.inputs[0];
          this.store.setCurrentInput(input);
          input.focus();
        }
      },

      restartTest() {
        this.pickInputIndexs();
        this.oldInputIndexs = [...this.inputIndexs]
        this.focusInput();
      }
    },
  };
</script>
