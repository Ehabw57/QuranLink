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
    modelValue: {type: Number, required:true}
  },
  emits: ['done', 'update:modelValue'],
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
        return;
      }
      this.activeIndex++;
      await this.focusInput();
      this.$refs.words[this.activeIndex - 1].classList.remove('correct');
      this.$emit('update:modelValue', questionVerse.surah_id)
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
  watch: {
    verses: {
      handler() {
        this.restartTest();
      },
      immediate: true
    }
  }
};
</script>
