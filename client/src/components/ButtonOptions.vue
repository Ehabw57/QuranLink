<template>
    <button 
      v-for="(item, index) in options" 
      :key="`option-${index}`" 
      :class="{ active: modelValue === item }"
      @click="updateValue(item)">
      {{ item }}
    </button>
</template>

<script>
export default {
  props: {
    options: { type: Array, required: true },
    modelValue: { type: String, required: true }
  },
  methods: {
    updateValue(newValue) {
      this.$emit('update:modelValue', newValue);
    }
  }
};
</script>

<style scoped>
.button-group {
  display: flex;
  gap: 8px;
}

button {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  font-size: 10px;
  padding: 4px 8px;
}

button.active {
  color: #cc2;
}
</style>

