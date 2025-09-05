<template>

  <header class="site-header">
    <div class="logo"></div>
    <h1>Quran Link</h1>
    <button class="lang-toggle" @click="toggleLanguage">{{ language === 'en' ? 'ع' : 'EN' }}</button>
    <i class="fa-solid" :class="[theme === 'dark' ? 'fa-sun' : 'fa-moon']" @click="toggleTheme"></i>
    <button class="settings" @click="isModalOpend = true" aria-label="Open settings">
      <i class="fa-solid fa-gear"></i>
    </button>
  </header>


  <div class="desktop-only config">
    <div class="config-item"><i class="fa-solid fa-layer-group" title="Mode"></i> <ButtonOptions :options="modes" v-model="mode" /></div>
    <div class="seprator"></div>
    <div class="config-item"><i class="fa-solid fa-sliders" title="Range Type"></i> <ButtonOptions :options="ranges" v-model="range" /></div>
    <div class="seprator"></div>
    <div class="config-item" v-if="range=='key'">
      <i class="fa-solid fa-book-open-reader" title="Verse Range"></i> <VerseSelector @change="fetchVerses" :chapters="chapters" v-model="verseRangeValue" />
    </div>
    <div class="config-item" v-else>
      <i class="fa-solid fa-hashtag" title="Numeric Range"></i>
      <RangeSelector @change="fetchVerses" :limit='rangeLimit' v-model="rangeValue"/>
    </div>
    <div class="seprator"></div>
  </div>


  <div v-show="isModalOpend"  class="modal"> 
    <i @click="isModalOpend = false" class="close fa-solid fa-xmark"></i>
    <div class="modal-content">

      <h1>Test Config</h1>

      <div>
        <i class="fa-solid fa-layer-group" title="Mode"></i>
        <ButtonOptions :options="modes" v-model="mode" />
      </div>

      <div>
        <i class="fa-solid fa-sliders" title="Range Type"></i>
        <ButtonOptions :options="ranges" v-model="range" />
      </div>

      <div v-if="range=='key'">
        <i class="fa-solid fa-book-open-reader" title="Verse Range"></i>
        <VerseSelector @change="fetchVerses" :chapters="chapters" v-model="verseRangeValue" />
      </div>
      <div v-else>
        <i class="fa-solid fa-hashtag" title="Numeric Range"></i>
        <RangeSelector @change="fetchVerses" :limit='rangeLimit' v-model="rangeValue"/>
      </div>
    </div>
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

  <footer class="site-footer">
    <span>CopyRight 2025 @Ehab Hegazy</span>
  </footer>

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
        loading: true,
        theme: 'dark',
        language: 'en'
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
      onEscKey(event) {
        if (event.key === 'Escape' && this.isModalOpend) {
          this.isModalOpend = false;
        }
      },
      applyTheme(theme) {
        const root = document.documentElement;
        const surahBorder = document.getElementsByClassName('border-image')[0];

        if (theme === 'light') {
          root.setAttribute('data-theme', 'light');
          surahBorder.style.backgroundImage = 'url("./assets/Surah-border-light.png")';
        } else {
          root.removeAttribute('data-theme');
          surahBorder.style.backgroundImage = 'url("./assets/Surah-border-dark.png")'

        }
        this.theme = theme;
        try { localStorage.setItem('theme', theme); } catch (e) {console.log(e)}
      },
      toggleTheme() {
        const next = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme(next);
      },
      applyLanguage(lang) {
        const root = document.documentElement;
        const dir = lang === 'ar' ? 'rtl' : 'ltr';
        root.setAttribute('lang', lang);
        root.setAttribute('dir', dir);
        this.language = lang;
        try {localStorage.setItem('language', lang); } catch (e) { console.log(e) }
      },
      toggleLanguage() {
        const next = this.language === 'ar' ? 'en' : 'ar';
        this.applyLanguage(next);
      },
      async fetchChapters() {
        this.loading = true;
        const response = await fetch("http://localhost:8000/surahs");
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

        const response = await fetch(`http://localhost:8000/verses?${params}`);
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
    mounted() {
      window.addEventListener('keydown', this.onEscKey);
      let initial = 'dark';
      try {
        const saved = localStorage.getItem('theme');
        if (saved === 'light' || saved === 'dark') initial = saved;
        else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) initial = 'light';
      } catch (e) {console.log(e)}
      this.applyTheme(initial);

      // Initialize language
      let initialLang = 'en';
      try {
        const savedLang = localStorage.getItem('language');
        if (savedLang === 'ar' || savedLang === 'en') initialLang = savedLang;
      } catch (e) { console.log(e) }
      this.applyLanguage(initialLang);
    },
    beforeUnmount() {
      window.removeEventListener('keydown', this.onEscKey);
    },
  }
</script>
