<template>
  <p class="quran-text" v-for="(word, index) in verses[0].text" :key="index">{{ word }}</p>
  <p class="quran-text">{{ verses[0].glyph_number }}</p>


  <div class="verseBlock" v-if="verses[1]">
    <div v-for="(word, index) in verses[1].text" :key="index">

      <inputBox
      v-if="activeIndex === index"
      ref="inputs"
      :expected="verses[1].simple_text[index]"
      @correct="handleCorrect()"
      />

      <p class="correct quran-text" v-else-if="activeIndex > index" ref="words">{{ word }}</p>
      <p class="dashes" v-else>{{ store.generateDashes(verses[1].simple_text[index].length) }}</p>

    </div>

    <p class="quran-text">{{ verses[1].glyph_number }}</p>
  </div>
</template>

<script>
  import { store } from '../store.js';

  export default {
    props: {
      verses: { type: Array, required: true },
    },
    emits: ['done'],
    data() {
      return {
        store,
        activeIndex: 0
      };
    },
    methods: {
      async handleCorrect() {
        const questionVerse = this.verses[1];
        if(this.activeIndex === questionVerse.text.length - 1) {
          this.$emit('done');
        } else {
          this.activeIndex++;
          await this.focusInput();
          const word = this.$refs.words[this.activeIndex - 1]
          await this.store.delay(600);
          word.classList.remove('correct');
        }
      },

      async focusInput() {
        await this.$nextTick();
        if (this.$refs.inputs?.length > 0){
          const input = this.$refs.inputs[0];
          this.store.setCurrentInput(input);
          input.focus();
        }
      },

      restartTest() {
        this.activeIndex = 0;
        this.focusInput();
      }
    },
  };
</script>
