<template>
  <div class="testContaner">
    <displayWord v-for="(word, index) in oriVerses[0].text" :key="index">{{ word }}</displayWord>
    <displayWord>{{ oriVerses[0].glyph_number }}</displayWord>
    <div class="verseBlock" v-for="(verse, verseIndex) in verses" :key="verse.id">
      <div class="wordContainer" v-for="(word, wordIndex) in verse.text" :key="wordIndex">
        <displayWord v-if="isWordCorrect(verseIndex, wordIndex)">{{ word }}</displayWord>

        <inputBox
          v-else-if="isCurrentInput(verseIndex, wordIndex)"
          :ref="`input-${verseIndex}-${wordIndex}`"
          :expected="verse.simple_text[wordIndex]"
          @correct="handleCorrect(verseIndex, wordIndex)"
        />

        <displayWord v-else>{{ store.generateDashes(verse.simple_text[wordIndex].length) }}</displayWord>
      </div>

      <displayWord>{{ verse.glyph_number }}</displayWord>
    </div>
  </div>
</template>

<script>
  import { store } from '../store.js';

export default {
  props: {
    oriVerses: { type: Array, required: true },
    modelValue: {type: Number, required:true}
  },
  data() {
    return {
      store,
      verses: [],
      activeVerse: 0, 
      activeWord: 0,    
      correctWords: {}  
    };
  },
  methods: {
    setUp() {
      this.activeVerse = 0;
      this.activeWord = 0;
      this.correctWords = {};
      this.verses = this.oriVerses.slice(1);
      this.$nextTick(() => {
        const firstInput = this.$refs[`input-0-0`]?.[0];
        this.store.setCurrentInput(firstInput);
        firstInput.focus();
      });
      this.$emit('update:modelValue', this.verses[this.activeVerse].surah_id)
    },
    isWordCorrect(verseIndex, wordIndex) {
      return this.correctWords[`${verseIndex}-${wordIndex}`];
    },
    isCurrentInput(verseIndex, wordIndex) {
      return verseIndex === this.activeVerse && wordIndex === this.activeWord;
    },
    handleCorrect(verseIndex, wordIndex) {
      this.correctWords[`${verseIndex}-${wordIndex}`] = true;

      if (wordIndex + 1 < this.verses[verseIndex].text.length) {
        this.activeWord++;
      } else {
        if (verseIndex + 1 < this.verses.length) {
          this.activeVerse++;
          this.activeWord = 0;
        } else {
          this.$emit('done');
        }
      }

      this.$nextTick(() => {
        const nextInput = this.$refs[`input-${this.activeVerse}-${this.activeWord}`]?.[0];
          this.store.setCurrentInput(nextInput);
          nextInput.focus();
      });
      this.$emit('update:modelValue', this.verses[this.activeVerse].surah_id)
    },
    restartTest() {
      this.activeVerse = 0;
      this.activeWord = 0;
      for (const key in this.correctWords) {
        this.correctWords[key] = false;
      }
      this.setUp()
    }
  },
  watch: {
    oriVerses: {
      handler() {
        this.setUp()
      },
       immediate: true
    }
  }
};
</script>

<style scoped>
.testContaner {
  display: flex;
  margin:0 auto;
  width: 70vw;
  flex-wrap: wrap; 
  justify-content: center; 
  direction: rtl; 
  overflow: hidden;
  height: 15.1vh;
}

.verseBlock {
  display: contents; 
}

.wordContainer {
  white-space: nowrap; 
}
    .dashes {
      font-size: 10px;
    }
</style>

