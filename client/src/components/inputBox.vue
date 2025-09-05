<template>
  <textarea 
    tabindex="1"
    rows='1'
    ref="input"
    class="input"
    :class="{'shake': isShaking}"
    type="textara"
    v-model="inputValue"
    @input="handleInput"
    :style="{ width: inputWidth }">
  </textarea>
</template>

  <script>
    export default {
      props: {
        expected :{
          type: String,
          required: true
        }
      },
      emits: ['correct'],
      data() {
        return {
          inputValue: '',
          hint: '',
          isShaking: false
        }
      },
      computed: {
        inputWidth() {
          return `${this.expected.length + 1}ch`;
        }
      },
      methods: {
        handleInput () {
          if (this.inputValue[this.inputValue.length -1] === ' '){
            this.addHint();
          }
          if (this.inputValue[this.inputValue.length -1] === '\n'){
            this.emitCorrect();
          }
          if (this.inputValue.length == this.expected.length) {
            if (this.simplifyText(this.inputValue) === this.simplifyText(this.expected)) {
              this.emitCorrect();
            } else {
              this.isShaking = true;
              setTimeout(() => {
                this.inputValue = this.hint;
                this.isShaking = false;
              },400)
            }
          }
        },
        addHint() {
          if (this.hint.length < this.expected.length - 1) {
            this.hint += this.expected[this.hint.length];
            this.inputValue = this.hint;
          } else {
            this.emitCorrect();
          }
        },
        simplifyText(text) {
          return text
            .replace(/[إأآ]/g, "ا")
            .replace(/ة/g, "ه")
            .replace(/ى/g, "ي");
        },
        emitCorrect() {
          this.$emit('correct');
          this.inputValue = '';
        },
        focus() {
          this.$refs.input.focus();
        }
      }
    }
  </script>

  <style scoped>


</style>
