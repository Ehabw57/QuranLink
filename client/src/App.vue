<template>
  <div class="desktop-only config">
    <ButtonOptions :options="modes" v-model="mode" />
    <div class="seprator"></div>
    <ButtonOptions :options="ranges" v-model="range" />
    <div class="seprator"></div>
    <VerseSelector @change="fetchVerses" v-if="range=='key'" :chapters="chapters" v-model="verseRangeValue" />
    <RangeSelector @change="fetchVerses" :limit='rangeLimit' v-else v-model="rangeValue"/>
    <div class="seprator"></div>
  </div>


  <div v-show="isModalOpend"  class="modal"> 
    <i @click="isModalOpend = false" class="close fa-solid fa-xmark"></i>
    <div class="modal-content">

      <h1>Test Config</h1>

      <div>
        <ButtonOptions :options="modes" v-model="mode" />
      </div>

      <div>
        <ButtonOptions :options="ranges" v-model="range" />
      </div>

      <VerseSelector @change="fetchVerses" v-if="range=='key'" :chapters="chapters" v-model="verseRangeValue" />
      <RangeSelector @change="fetchVerses" :limit='rangeLimit' v-else v-model="rangeValue"/>
    </div>
  </div>

  <div @click="isModalOpend = true" class="mobile-only config">
    <i class="fa-solid fa-gear"></i>
    <label>Test Config</label>
  </div>



  <div class="border-container">
    <SurahBorder :surahName="surahName" />
  </div>


  <div class="test-container" v-if="!loading && verses[activeVerse]">

    <div class="verses-test" v-if="mode === 'verses'">
    <testVerse  ref="verseTest" @done="handelDone" :verses="slicedVerses" />
    </div>

    <div class="words-test" v-else >
      <testWord  ref="wordsTest" @done="handelDone"  :verse="verses[activeVerse]" />
    </div>

  </div>

  <div class="loader-container" v-else>
    <span class="loader"></span>
  </div>


  <div class="test-buttons">
<i class="fa-solid fa-repeat" :class="{ active: isRepeat }" @click="isRepeat = !isRepeat"></i>

    <i class="fa-solid fa-shuffle" @click="getRandomVerse"></i>
    <i class="fa-solid fa-rotate-right" @click="restart"></i>
    <i class="fa-solid fa-angles-left" @click="handelDone"></i>
  </div>

</template>

<script>
import {store} from './store.js';
  export default {
    name: 'App',
    data () {
      return {
        store,
        chapters: [],
        verses: [],
        activeVerse: 0,
        isRepeat: false,
        isModalOpend: false,
        modes: ['words', 'verses'],
        mode: 'words',
        ranges: ['juz', 'page', 'key'],
        range: 'page',
        rangeValue: {start: 3, end:4},
        verseRangeValue: {startChapter: 1, startVerse: 1, endChapter: 1, endVerse: 7},
        loading: true
      }
    },
    computed: {
      rangeLimit() {
        return this.range === 'page' ? 604 : 30
      },

      surahName() {
        if (!this.loading) {
          return this.chapters.find(s => s.id === this.verses[this.activeVerse].surah_id).name
        }
        return "loading...";
      },

      slicedVerses() {
          return this.verses.slice(this.activeVerse)
      }
    },

    methods: {
      async fetchChapters() {
        this.loading = true;
        const response = await fetch("http://192.168.1.72:8000/surahs");
        this.chapters = await response.json();
      },

      async fetchVerses() {
        this.loading = true;
        const { startChapter, startVerse, endChapter, endVerse } = this.verseRangeValue;
        const { start, end } = this.rangeValue;
        const params = new URLSearchParams({
          range_type: this.range,
          range_value: this.range === "key" ? `${startChapter}:${startVerse}-${endChapter}:${endVerse}` : `${start}:${end}`,
        }).toString();

        const response = await fetch(`http://192.168.1.72:8000/verses?${params}`);
        this.verses = await response.json();

        this.activeVerse = 0;
        this.loading = false;
        await this.$nextTick();
        this.restart();
      },

      getRandomVerse() {
        this.activeVerse = Math.floor(Math.random() * (this.verses.length - 1));
        this.restart();
      },

      async handelDone() {
        if (!this.isRepeat) {
          this.activeVerse = (this.activeVerse + 1) % this.verses.length;
        }
        await this.$nextTick();
        this.restart();
      },

      restart(){
        if (!this.$refs.wordsTest && !this.$refs.verseTest) {
          return;
        }
        this.mode === 'words'
          ?this.$refs.wordsTest.restartTest() 
          :this.$refs.verseTest.restartTest();
      },
    },

    async created() {
      await this.fetchChapters()
      await this.fetchVerses()
    },
  }
</script>
