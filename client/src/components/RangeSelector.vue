<template>
  <div>
    <label for="start">Start:</label>
    <select id="start" :value="modelValue.start" @change="updateStart($event.target.value)">
      <option v-for="i in limit" :key="i" :value="i">{{ i }}</option>
    </select>

    <label for="end">End:</label>
    <select id="end" :value="modelValue.end" @change="updateEnd($event.target.value)">
      <option v-for="i in limit" :key="i" :value="i">{{ i }}</option>
    </select>
  </div>
</template>

<script>
export default {
  props: {
    limit: {
      type: Number,
      required: true,
    },
    modelValue: {
      type: Object,
      required: true,
    },
  },
  methods: {
    updateStart(newStart) {
      const start = Number(newStart);
      const end = Math.max(start, this.modelValue.end);
      this.$emit('update:modelValue', { start, end });
    },
    updateEnd(newEnd) {
      const end = Number(newEnd);
      const start = Math.min(end, this.modelValue.start);
      this.$emit('update:modelValue', { start, end });
    },
  },
};
</script>

