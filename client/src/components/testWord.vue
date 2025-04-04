<template>
  <div class='verseContainer'>
  <div v-for="(word, index) in verse.simple_text" :key="index">
    <inputBox
    v-if="isCurrentInput(index)"
    ref="input"
    @correct="handleCorrect(index)"
    :expected="word"
    />
    <displayWord v-else-if="isDisplayed(index)">{{ verse.text[index] }}</displayWord>
    <label v-else>{{ store.generateDashes(word.length) }}</label>
  </div>
  <displayWord>{{ verse.glyph_number }}</displayWord>
  </div>
</template>

<script>
  import { store } from '../store.js';

  export default { 
    props : {
      verse: {type: Object, required: true},
      modelValue: {type: Number, required:true}
    },
    data () {
      return {
        store,
        currentInput:  0,
        activeIndex: 0,
        arrayMap: [],
        correctWords: {}
      }
    },
    methods: {
      focusInput() {
        this.$nextTick(() => {
          const nextInput = this.$refs.input[0];
          if(nextInput) {
          this.store.setCurrentInput(nextInput);
          nextInput.focus();
          }
        });
      },
      isCurrentInput(index) {
        return this.arrayMap.includes(index) && this.currentInput === index;
      },
      isDisplayed(index) {
        return !this.arrayMap.includes(index) || this.correctWords[index]
      },
      handleCorrect(index) {
        this.correctWords[index] = true;
        this.activeIndex++;
        this.currentInput = this.arrayMap[this.activeIndex];
        if (this.currentInput) {
          this.focusInput();
        } else {
          this.$emit('done');
        }
      },
      createMap() {
        const verseLength = this.verse.text.length;
        if (verseLength > 1) {
        const arrayLength = Math.floor(verseLength * 0.50);
        let map = Array.from({length: verseLength}, (_, i) => i );
        this.arrayMap = this.store.shuffleArray(map).slice(0, arrayLength).sort((a, b) => a - b);
        this.currentInput = this.arrayMap[0];
        } else {
          this.arrayMap = [0];
          this.currentInput = 0;
        }
        this.$emit('update:modelValue', this.verse.surah_id)
      },
      restartTest() {
        this.activeIndex = 0;
        this.currentInput = 0;
        this.correctWords = {};
        this.createMap();
        this.focusInput();
      }
    },
    watch: {
      verse: {
        handler() {
          this.createMap();
          this.focusInput();
        },
        deep: true,
       immediate: true
      }
    }
  }
</script>
<style>
.verseContainer {
  display: flex;
  direction: rtl;
  justify-content: center;
  gap: 1px;
}
</style>
