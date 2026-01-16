<template>
  <div style="display: flex; gap: 10px; align-items: center;">
    <span>
      <label for="start">{{ t('labels.start') }}:</label>
      <select id="start" :value="modelValue.start" @change="updateStart($event.target.value)">
        <option v-for="i in limit" :key="i" :value="i">{{ i }}</option>
      </select>
    </span>

    <component :is="locale === 'ar' ? 'ArrowLeft' : 'ArrowRight'" style="width: 18px; height: 18px; color: var(--color-muted)" />

    <span>
      <label for="end">{{ t('labels.end') }}:</label>
      <select id="end" :value="modelValue.end" @change="updateEnd($event.target.value)">
        <option v-for="i in limit" :key="i" :value="i">{{ i }}</option>
      </select>
    </span>
  </div>
</template>

<script>
import { useLanguage } from '@/composables/useLanguage';
import { ArrowLeft, ArrowRight } from 'lucide-vue-next';

export default {
  name: 'RangeInput',
  components: { ArrowLeft, ArrowRight},
  props: {
    limit: { type: Number, required: true },
    modelValue: { type: Object, required: true },
  },
  emits: ['update:modelValue', 'change'],
  setup() {
    const { locale, t } = useLanguage();
    return {locale, t };
  },
  methods: {
    updateStart(newStart) {
      const start = Number(newStart);
      const end = Math.max(start, this.modelValue.end);
      this.$emit('update:modelValue', { start, end });
      this.$emit('change');
    },
    updateEnd(newEnd) {
      const end = Number(newEnd);
      const start = Math.min(end, this.modelValue.start);
      this.$emit('update:modelValue', { start, end });
      this.$emit('change');
    },
  },
};
</script>
