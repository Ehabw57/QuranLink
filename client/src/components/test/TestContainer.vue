<template>
  <div class="test-container" v-if="!isLoading && currentVerse">
    <VerseTest 
      v-if="mode === 'verses'"
      ref="verseTestRef"
      :verses="slicedVerses"
      @done="$emit('done')"
    />
    <WordTest 
      v-else
      ref="wordTestRef"
      :verse="currentVerse"
      @done="$emit('done')"
    />
  </div>
  <LoadingSpinner v-else />
</template>

<script>
import { ref, nextTick } from 'vue';
import VerseTest from './VerseTest.vue';
import WordTest from './WordTest.vue';
import LoadingSpinner from '@/components/ui/LoadingSpinner.vue';

export default {
  name: 'TestContainer',
  components: { VerseTest, WordTest, LoadingSpinner },
  props: {
    mode: { type: String, required: true },
    isLoading: { type: Boolean, required: true },
    currentVerse: { type: Object, default: null },
    slicedVerses: { type: Array, required: true },
  },
  emits: ['done'],
  setup(props, { expose }) {
    const verseTestRef = ref(null);
    const wordTestRef = ref(null);
    
    const restart = async () => {
      await nextTick();
      if (props.mode === 'words' && wordTestRef.value) {
        wordTestRef.value.restartTest();
      } else if (props.mode === 'verses' && verseTestRef.value) {
        verseTestRef.value.restartTest();
      }
    };
    
    expose({ restart });
    
    return { verseTestRef, wordTestRef };
  },
};
</script>
