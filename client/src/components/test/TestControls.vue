<template>
  <div class="test-buttons">
    <button class="icon-btn" :class="{ active: isRepeat }" @click="$emit('toggleRepeat')" :title="$t('buttons.repeat')">
      <Repeat />
    </button>
    <button class="icon-btn" @click="$emit('shuffle')" :title="$t('buttons.shuffle')">
      <Shuffle />
    </button>
    <button class="icon-btn" @click="$emit('restart')" :title="$t('buttons.restart')">
      <RotateCw />
    </button>
    <button class="icon-btn" @click="$emit('next')" :title="$t('buttons.next')">
      <ChevronLeft />
    </button>
  </div>
</template>

<script>
import { Repeat, Shuffle, RotateCw, ChevronLeft } from 'lucide-vue-next';

export default {
  name: 'TestControls',
  components: { Repeat, Shuffle, RotateCw, ChevronLeft },
  props: {
    isRepeat: { type: Boolean, required: true },
  },
  emits: ['toggleRepeat', 'shuffle', 'restart', 'next'],
};
</script>
