<template>
  <div class="select-boxes">
    <select @change="updateModel('sc', $event.target.value)" :value="modelValue.sc">
      <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
        {{ chapter.id }}-{{ chapter.name }}
      </option>
    </select>
    <select @change="updateModel('sv', $event.target.value)" :value="modelValue.sv">
      <option v-for="n in startVerseOptions" :key="n" :value="n">{{ n }}</option>
    </select>


    <select @change="updateModel('ec', $event.target.value)" :value="modelValue.ec">
      <option v-for="chapter in filteredChapters" :key="chapter.id" :value="chapter.id">
        {{ chapter.id }}-{{ chapter.name }}
      </option>
    </select>
    <select @change="updateModel('ev', $event.target.value)" :value="modelValue.ev">
      <option v-for="n in endVerseOptions" :key="n" :value="n">{{ n }}</option>
    </select>
  </div>
</template>

<script>
export default {
  props: {
    chapters: {
      type: Array,
      required: true,
    },
    modelValue: {
      type: Object,
      required: true,
    },
  },
  computed: {
    filteredChapters() {
      return this.chapters.filter(chapter => chapter.id >= this.modelValue.sc);
    },
    startVerseOptions() {
      const startChapter = this.chapters.find(ch => ch.id === this.modelValue.sc);
      return startChapter ? Array.from({ length: startChapter.ayahs_count }, (_, i) => i + 1) : [];
    },
    endVerseOptions() {
      const endChapter = this.chapters.find(ch => ch.id === this.modelValue.ec);
      if (!endChapter) return [];
      const start = this.modelValue.sc === this.modelValue.ec ? this.modelValue.sv : 1;
      return Array.from({ length: endChapter.ayahs_count - start + 1 }, (_, i) => i + start);
    },
  },
  methods: {
    updateModel(key, value) {
      value = Number(value);
      let updatedValue = { ...this.modelValue, [key]: value };

      if (key === "sc") {
        if (updatedValue.sc > updatedValue.ec) updatedValue.ec = updatedValue.sc;
        const startChapter = this.chapters.find(ch => ch.id === updatedValue.sc);
        if (startChapter && updatedValue.sv > startChapter.ayahs_count) {
          updatedValue.sv = startChapter.ayahs_count;
        }
      }

      if (key === "ec") {
        const endChapter = this.chapters.find(ch => ch.id === updatedValue.ec);
        if (endChapter && updatedValue.ev > endChapter.ayahs_count) {
          updatedValue.ev = endChapter.ayahs_count;
        }
      }

      if (updatedValue.sc === updatedValue.ec && updatedValue.sv > updatedValue.ev) {
        updatedValue.ev = updatedValue.sv;
      }

      const endChapter = this.chapters.find(ch => ch.id === updatedValue.ec);
      if (endChapter && updatedValue.ev > endChapter.ayahs_count) {
        updatedValue.ev = endChapter.ayahs_count;
      }

      this.$emit("update:modelValue", updatedValue);
    },
  },
};
</script>
