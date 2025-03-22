<template>
  <div class="testContainer">
  <div class="testContainer" v-for="(word, index) in verse.text" :key="index" >
    <displayWord  v-if="activeIndex > index">{{ word }}</displayWord>
    <inputBox :ref="`input${index}`" :expected="simpleText[index]" v-else-if="activeIndex === index" @correct="handleCorrect" />
    <label v-else >{{ getDashes(index) }}</label>
  </div>
  <displayWord>{{verse.glyph}}</displayWord>
  </div>
</template>

<script>
  import { store } from '../store.js';

  export default {
    props: {
      verse: { type: Object, required: true }
    },
    data() {
      return {
        store
      }
    },
    computed: {
      activeIndex() {
        return this.store.currentInputIndex
      },
      simpleText() {
      return this.verse.simple_text;
      }
    },
    methods: {
      getDashes(index) {
        return '-'.repeat(this.verse.simple_text[index].length);
      },
      handleCorrect() {
          this.store.incrementIndex();
        if (this.activeIndex < this.simpleText.length) {
          this.$nextTick(() => {
            const nextInput = this.$refs[`input${this.activeIndex}`][0];
            nextInput.focus();
          });
        }
      },
    }
  }
</script>
<style scoped>
div.testContainer {
  display: flex;
  justify-content: flex-start;
  flex-direction: row-reverse;
  gap: 5px;
}

</style>
