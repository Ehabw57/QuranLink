<template>
  <div class="config-panel" >
    
    <div class="config-item">
      <label v-if="variant === 'modal'">{{ t('config.rangeType') }}</label>
      <ButtonGroup 
        :options="rangeOptions"
        :modelValue="rangeType"
        @update:modelValue="$emit('update:rangeType', $event)"
        labelPrefix="ranges"
      />
    </div>
    
    <div class="config-item">
      <component :is="rangeType === 'key' ? BookOpen : Hash" :title="rangeType === 'key' ? t('config.verseRange') : t('config.numericRange')" />
      <label v-if="variant === 'modal'">
        {{ rangeType === 'key' ? t('config.verseRange') : t('config.numericRange') }}
      </label>
      
      <VerseRangeInput 
        v-if="rangeType === 'key'"
        :chapters="chapters"
        :modelValue="verseRangeValue"
        @update:modelValue="$emit('update:verseRangeValue', $event)"
        @change="$emit('rangeChange')"
      />
      <RangeInput 
        v-else
        :limit="rangeLimit"
        :modelValue="rangeValue"
        @update:modelValue="$emit('update:rangeValue', $event)"
        @change="$emit('rangeChange')"
      />
    </div>
  </div>
</template>

<script>
import { useLanguage } from '@/composables/useLanguage';
import {  BookOpen, Hash, Layers, Key } from 'lucide-vue-next';
import ButtonGroup from '@/components/ui/ButtonGroup.vue';
import RangeInput from '@/components/ui/RangeInput.vue';
import VerseRangeInput from '@/components/config/VerseRangeInput.vue';

export default {
  name: 'ConfigPanel',
  components: { ButtonGroup, RangeInput, VerseRangeInput, BookOpen, Hash, Layers, Key },
  props: {
    variant: { type: String, default: 'desktop' }, // 'desktop' | 'modal'
    rangeType: { type: String, required: true },
    rangeValue: { type: Object, required: true },
    verseRangeValue: { type: Object, required: true },
    rangeLimit: { type: Number, required: true },
    chapters: { type: Array, required: true },
  },
  setup() {
    const { t } = useLanguage();
    const rangeOptions = [
      { name: 'juz', icon: Layers },
      { name: 'page', icon: BookOpen },
      { name: 'key', icon: Key },
    ];
    return { t, rangeOptions };
  },
};
</script>
