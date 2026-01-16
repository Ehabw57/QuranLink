<template>
  <AppHeader v-model:mode="mode" @openSettings="isModalOpen = true" />

  <ConfigPanel class="desktop-only config" variant="desktop" v-model:rangeType="rangeType"
    v-model:rangeValue="rangeValue" v-model:verseRangeValue="verseRangeValue" :rangeLimit="rangeLimit"
    :chapters="chapters" @rangeChange="fetchVerses" />

  <AppModal v-model="isModalOpen" :title="t('modal.testConfig')">
    <ConfigPanel variant="modal" v-model:rangeType="rangeType" v-model:rangeValue="rangeValue"
      v-model:verseRangeValue="verseRangeValue" :rangeLimit="rangeLimit" :chapters="chapters"
      @rangeChange="fetchVerses" />
  </AppModal>

  <div class="border-container">
    <SurahBorder :surahName="surahName" />
  </div>

  <TestContainer ref="testContainerRef" :mode="mode" :isLoading="isLoading" :currentVerse="currentVerse"
    :slicedVerses="slicedVerses" @done="handleDone" />

  <TestControls :isRepeat="isRepeat" @toggleRepeat="isRepeat = !isRepeat" @shuffle="randomVerse(); restart()"
    @restart="restart" @next="handleDone" />

  <AppFooter />
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue';
import { useToast } from 'vue-toastification';

// Layout
import AppHeader from '@/components/layout/AppHeader.vue';
import AppFooter from '@/components/layout/AppFooter.vue';
import AppModal from '@/components/layout/AppModal.vue';

// Features
import ConfigPanel from '@/components/config/ConfigPanel.vue';
import TestContainer from '@/components/test/TestContainer.vue';
import TestControls from '@/components/test/TestControls.vue';
import SurahBorder from '@/components/quran/SurahBorder.vue';

// Composables
import { useTheme } from '@/composables/useTheme';
import { useLanguage } from '@/composables/useLanguage';
import { useQuranTest } from '@/composables/useQuranTest';

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter,
    AppModal,
    ConfigPanel,
    TestContainer,
    TestControls,
    SurahBorder,
  },
  setup() {
    const toast = useToast();
    const { initTheme } = useTheme();
    const { t, initLanguage } = useLanguage();

    const {
      chapters,
      isRepeat,
      isLoading,
      mode,
      rangeType,
      rangeValue,
      verseRangeValue,
      currentVerse,
      slicedVerses,
      rangeLimit,
      currentSurahName,
      fetchChapters,
      fetchVerses: fetchVersesAction,
      nextVerse,
      randomVerse,
    } = useQuranTest();

    const testContainerRef = ref(null);
    const isModalOpen = ref(false);

    const surahName = computed(() => {
      if (!currentSurahName.value) return t('loading');
      return currentSurahName.value.name;
    });

    const fetchVerses = async () => {
      try {
        await fetchVersesAction();
        await nextTick();
        restart();
      } catch (e) {
        const message = e.isNetworkError
          ? t('errors.networkError')
          : e.isServerError
            ? t('errors.serverError')
            : t('errors.fetchVersesError');
        toast.error(message);
      }
    };

    const handleDone = async () => {
      nextVerse();
      await nextTick();
      restart();
    };

    const restart = () => {
      testContainerRef.value?.restart();
    };

    const init = async () => {
      try {
        await fetchChapters();
        await fetchVerses();
      } catch (e) {
        toast.error(t('errors.fetchChaptersError'));
      }
    };

    onMounted(() => {
      initTheme();
      initLanguage();
      init();
    });

    return {
      t,
      // State
      chapters,
      isLoading,
      isRepeat,
      isModalOpen,

      // Config
      mode,
      rangeType,
      rangeValue,
      verseRangeValue,
      rangeLimit,

      // Computed
      currentVerse,
      slicedVerses,
      surahName,

      // Refs
      testContainerRef,

      // Methods
      fetchVerses,
      handleDone,
      restart,
      randomVerse,
    };
  },
};
</script>
