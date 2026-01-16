<template>
  <div class="selector">
  <div>
    <label>{{ t('labels.start') }}:</label>
    <select @change="updateModel('startChapter', $event.target.value)" :value="modelValue.startChapter">
      <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
        {{ chapter.id }}-{{ locale === 'ar' ? chapter.name : chapter.en_name }}
      </option>
    </select>
    <select @change="updateModel('startVerse', $event.target.value)" :value="modelValue.startVerse">
      <option v-for="n in startVerseOptions" :key="n" :value="n">{{ n }}</option>
    </select>
  </div>

      <component :is="locale === 'ar' ? 'ArrowLeft' : 'ArrowRight'" style="width: 18px; height: 18px; color: var(--color-muted)" />

  <div>
    <label>{{ t('labels.end') }}:</label>
    <select @change="updateModel('endChapter', $event.target.value)" :value="modelValue.endChapter">
      <option v-for="chapter in filteredChapters" :key="chapter.id" :value="chapter.id">
        {{ chapter.id }}-{{ locale === 'ar' ? chapter.name : chapter.en_name }}
      </option>
    </select>
    <select @change="updateModel('endVerse', $event.target.value)" :value="modelValue.endVerse">
      <option v-for="n in endVerseOptions" :key="n" :value="n">{{ n }}</option>
    </select>
  </div>
  </div>
</template>

<script>
import { useLanguage } from '@/composables/useLanguage';
import { ArrowLeft, ArrowRight } from 'lucide-vue-next';

export default {
  name: 'VerseRangeInput',
  components: { ArrowLeft, ArrowRight },
  props: {
    chapters: { type: Array, required: true },
    modelValue: { type: Object, required: true },
  },
  emits: ['update:modelValue', 'change'],
  setup() {
    const { locale, t } = useLanguage();
    return { locale, t };
  },
  computed: {
    filteredChapters() {
      return this.chapters.filter(chapter => chapter.id >= this.modelValue.startChapter);
    },
    startVerseOptions() {
      const startChapter = this.chapters.find(ch => ch.id === this.modelValue.startChapter);
      return startChapter ? Array.from({ length: startChapter.ayahs_count }, (_, i) => i + 1) : [];
    },
    endVerseOptions() {
      const endChapter = this.chapters.find(ch => ch.id === this.modelValue.endChapter);
      if (!endChapter) return [];
      const start = this.modelValue.startChapter === this.modelValue.endChapter ? this.modelValue.startVerse : 1;
      return Array.from({ length: endChapter.ayahs_count - start + 1 }, (_, i) => i + start);
    },
  },
  methods: {
    updateModel(key, value) {
      value = Number(value);
      let updatedValue = { ...this.modelValue, [key]: value };

      if (key === 'startChapter') {
        if (updatedValue.startChapter > updatedValue.endChapter) updatedValue.endChapter = updatedValue.startChapter;
        const startChapter = this.chapters.find(ch => ch.id === updatedValue.startChapter);
        if (startChapter && updatedValue.startVerse > startChapter.ayahs_count) {
          updatedValue.startVerse = startChapter.ayahs_count;
        }
      }

      if (key === 'endChapter') {
        const endChapter = this.chapters.find(ch => ch.id === updatedValue.endChapter);
        if (endChapter && updatedValue.endVerse > endChapter.ayahs_count) {
          updatedValue.endVerse = endChapter.ayahs_count;
        }
      }

      if (updatedValue.startChapter === updatedValue.endChapter && updatedValue.startVerse > updatedValue.endVerse) {
        updatedValue.endVerse = updatedValue.startVerse;
      }

      const endChapter = this.chapters.find(ch => ch.id === updatedValue.endChapter);
      if (endChapter && updatedValue.endVerse > endChapter.ayahs_count) {
        updatedValue.endVerse = endChapter.ayahs_count;
      }

      this.$emit('update:modelValue', updatedValue);
      this.$emit('change', updatedValue);
    },
  },
};
</script>

<style >
.selector {
  display: flex;
  align-items: center;
  gap: 12px;
}

label {
  margin-left: 4px;
  font-weight: 300;
  color: var(--color-muted);

}
</style>
