<template>
    <button 
      v-for="(item, index) in options" 
      :key="`option-${index}`" 
      :class="{ active: modelValue === item }"
      @click="updateValue(item)">
      {{ getLabel(item) }}
    </button>
</template>

<script>
import { useI18n } from 'vue-i18n';
export default {
  props: {
    options: { type: Array, required: true },
    modelValue: { type: String, required: true }
  },
  setup() {
    const { t, te } = useI18n();
    return { t, te };
  },
  methods: {
    updateValue(newValue) {
      this.$emit('update:modelValue', newValue);
    },
    getLabel(item) {
      // Check if translation exists for modes
      const modeKey = `modes.${item}`;
      if (this.te(modeKey)) {
        return this.t(modeKey);
      }
      
      // Check if translation exists for ranges
      const rangeKey = `ranges.${item}`;
      if (this.te(rangeKey)) {
        return this.t(rangeKey);
      }
      
      // Fallback to the item itself
      return item;
    }
  }
};
</script>
