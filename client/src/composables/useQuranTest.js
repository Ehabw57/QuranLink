import { ref, computed } from 'vue';
import { quranService } from '@/services/quranService';
import { RANGE_LIMITS } from '@/constants';

export function useQuranTest() {
  // State
  const chapters = ref([]);
  const verses = ref([]);
  const activeVerseIndex = ref(0);
  const isRepeat = ref(false);
  const isLoading = ref(true);
  const error = ref(null);
  
  // Config
  const mode = ref('words'); // 'words' | 'verses'
  const rangeType = ref('page'); // 'juz' | 'page' | 'key'
  const rangeValue = ref({ start: 3, end: 4 });
  const verseRangeValue = ref({
    startChapter: 1,
    startVerse: 1,
    endChapter: 1,
    endVerse: 7,
  });
  
  // Computed
  const currentVerse = computed(() => verses.value[activeVerseIndex.value]);
  const slicedVerses = computed(() => verses.value.slice(activeVerseIndex.value));
  const rangeLimit = computed(() => rangeType.value === 'page' ? RANGE_LIMITS.PAGE : RANGE_LIMITS.JUZ);
  
  const currentSurahName = computed(() => {
    if (isLoading.value || !chapters.value.length || !currentVerse.value) {
      return null;
    }
    return chapters.value.find(s => s.id === currentVerse.value.surah_id);
  });
  
  // Actions
  const fetchChapters = async () => {
    try {
      chapters.value = await quranService.getChapters();
    } catch (e) {
      error.value = e;
      throw e;
    }
  };
  
  const fetchVerses = async () => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const rangeValueStr = quranService.buildRangeValue(
        rangeType.value,
        rangeType.value === 'key' ? verseRangeValue.value : rangeValue.value
      );
      
      verses.value = await quranService.getVerses({
        rangeType: rangeType.value,
        rangeValue: rangeValueStr,
      });
      
      activeVerseIndex.value = 0;
    } catch (e) {
      error.value = e;
      throw e;
    } finally {
      isLoading.value = false;
    }
  };
  
  const nextVerse = () => {
    if (!isRepeat.value) {
      activeVerseIndex.value = (activeVerseIndex.value + 1) % verses.value.length;
    }
  };
  
  const randomVerse = () => {
    activeVerseIndex.value = Math.floor(Math.random() * verses.value.length);
  };
  
  return {
    // State
    chapters,
    verses,
    activeVerseIndex,
    isRepeat,
    isLoading,
    error,
    
    // Config
    mode,
    rangeType,
    rangeValue,
    verseRangeValue,
    
    // Computed
    currentVerse,
    slicedVerses,
    rangeLimit,
    currentSurahName,
    
    // Actions
    fetchChapters,
    fetchVerses,
    nextVerse,
    randomVerse,
  };
}
