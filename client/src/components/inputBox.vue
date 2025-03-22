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
            const errorRate = this.leDistance(this.inputValue, this.expected) / this.expected.length * 100;
            if (errorRate < 15) {
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
          }
        },
        leDistance(a, b) {
          const matrix = [];

          for (let i = 0; i <= a.length; i++) {
            matrix[i] = [i];
          }
          for (let j = 0; j <= b.length; j++) {
            matrix[0][j] = j;
          }

          for (let i = 1; i <= a.length; i++) {
            for (let j = 1; j <= b.length; j++) {
              const cost = a[i - 1] === b[j - 1] ? 0 : 1;
              matrix[i][j] = Math.min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost
              );
            }
          }

          return matrix[a.length][b.length];
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
}

input:focus {
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
  padding: 0;
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
