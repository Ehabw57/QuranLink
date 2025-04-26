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
