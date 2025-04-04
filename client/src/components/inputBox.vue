<template>
  <input 
  ref="input"
  :class="{'shake': isShaking}"
  type="text"
  v-model="inputValue"
  @input="handleInput"
  @keydown="handleKeydown"
  :style="{ width: inputWidth }">
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
          return `${this.expected.length}ch`;
        }
      },
      methods: {
        handleInput () {
          this.inputValue = this.inputValue.trim();
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
        handleKeydown(event) {
          if (event.shiftKey) {
            if (event.code === 'Enter') this.emitCorrect();
            if (event.code === 'Space') this.addHint();
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

input {
  background-color: transparent;
  border: 1px solid #ccc;
  outline: none;
  text-align: center;
  transition: all 0.3s ease;
  padding: 0;
  height: 20px;
  font-size: 12px;
  font-family: "Uthmani";
}

input:focus {
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.shake {
  position: relative;
  animation: shake 0.4s ease-in-out;
}

@keyframes shake {
  0%, 100% { color: black; background-color: transparent; left: 0; }
  25% { left: -4px; }
  50% { color: white; background-color: #e20; left: 4px; }
  75% { left: -4px; }
}
</style>
