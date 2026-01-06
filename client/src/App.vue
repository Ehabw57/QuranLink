<template>

  <header class="site-header">
    <div class="logo"></div>
    <h1>{{ $t('app.title') }}</h1>
    <button class="lang-toggle" @click="toggleLanguage">{{ locale === 'en' ? 'ع' : 'EN' }}</button>
    <i class="fa-solid" :class="[theme === 'dark' ? 'fa-sun' : 'fa-moon']" @click="toggleTheme"></i>
    <button class="settings" @click="isModalOpend = true" :aria-label="$t('header.settings')">
      <i class="fa-solid fa-gear"></i>
    </button>
  </header>


  <div class="desktop-only config">
    <div class="config-item"><i class="fa-solid fa-layer-group" :title="$t('config.mode')"></i> <ButtonOptions :options="modeOptions" v-model="mode" /></div>
    <div class="config-item"><i class="fa-solid fa-sliders" :title="$t('config.rangeType')"></i> <ButtonOptions :options="rangeOptions" v-model="range" /></div>
    <div class="config-item" v-if="range=='key'">
      <i class="fa-solid fa-book-open-reader" :title="$t('config.verseRange')"></i> <VerseSelector @change="fetchVerses" :chapters="chapters" v-model="verseRangeValue" />
    </div>
    <div class="config-item" v-else>
      <i class="fa-solid fa-hashtag" :title="$t('config.numericRange')"></i>
      <RangeSelector @change="fetchVerses" :limit='rangeLimit' v-model="rangeValue"/>
    </div>
  </div>


  <div v-show="isModalOpend"  class="modal" @click.self="isModalOpend = false"> 
    <div class="modal-content">
      <i @click="isModalOpend = false" class="close fa-solid fa-xmark"></i>

      <h1>{{ $t('modal.testConfig') }}</h1>

      <div>
        <label>
          <i class="fa-solid fa-layer-group"></i>
          {{ $t('config.mode') }}
        </label>
        <ButtonOptions :options="modeOptions" v-model="mode" />
      </div>

      <div>
        <label>
          <i class="fa-solid fa-sliders"></i>
          {{ $t('config.rangeType') }}
        </label>
        <ButtonOptions :options="rangeOptions" v-model="range" />
      </div>

      <div v-if="range=='key'">
        <label>
          <i class="fa-solid fa-book-open-reader"></i>
          {{ $t('config.verseRange') }}
        </label>
        <VerseSelector @change="fetchVerses" :chapters="chapters" v-model="verseRangeValue" />
      </div>
      <div v-else>
        <label>
          <i class="fa-solid fa-hashtag"></i>
          {{ $t('config.numericRange') }}
        </label>
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
    <div class="footer-content">
      <div class="footer-about">
        <h3>{{ $t('app.title') }}</h3>
        <p>{{ $t('footer.about') }}</p>
        <div class="footer-visits" v-if="visitCount !== null" aria-hidden="false" title="Visits">
          <i class="fa-solid fa-eye"></i>
          <span class="visit-count">{{ visitCount }}</span>
        </div>
      </div>
      <div class="footer-social">
        <div class="social-links">
          <a href="https://github.com/Ehabw57" target="_blank" rel="noopener noreferrer" aria-label="GitHub Profile">
            <i class="fa-brands fa-github"></i>
          </a>
          <a href="https://github.com/Ehabw57/QuranLink/" target="_blank" rel="noopener noreferrer" aria-label="Project Repository">
            <i class="fa-solid fa-code-branch"></i>
          </a>
          <a href="https://www.linkedin.com/in/ehababdelrady" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
            <i class="fa-brands fa-linkedin"></i>
          </a>
          <a href="https://ehabw57.github.io/personal_portofolio/" target="_blank" rel="noopener noreferrer" aria-label="Portfolio">
            <i class="fa-solid fa-globe"></i>
          </a>
          <a href="https://www.youtube.com/@mercy_world57" target="_blank" rel="noopener noreferrer" aria-label="YouTube">
            <i class="fa-brands fa-youtube"></i>
          </a>
        </div>
      </div>
    </div>
  </footer>

</template>

<script>
import {store} from './store.js';
import { useI18n } from 'vue-i18n';
import { useToast } from "vue-toastification";

  export default {
    name: 'App',
    setup() {
      const { locale, t } = useI18n();
      const toast = useToast();
      return { locale, t, toast };
    },
    data () {
      return {
        store,
        chapters: [],
        verses: [],
        activeVerse: 0,
        isRepeat: false,
        isModalOpend: false,
        mode: 'words',
        range: 'page',
        rangeValue: {start: 3, end:4},
        verseRangeValue: {startChapter: 1, startVerse: 1, endChapter: 1, endVerse: 7},
        loading: true,
        theme: 'dark',
        visitCount: null,
        // Use runtime-injected API URL if available (injected by server),
        // otherwise fall back to build-time env or localhost.
        apiUrl: (typeof window !== 'undefined' && window.__API_URL__) || process.env.VUE_APP_API_URL || 'http://localhost:8000'
      }
    },
    computed: {
      modeOptions() {
        return ['words', 'verses'];
      },
      rangeOptions() {
        return ['juz', 'page', 'key'];
      },
      rangeLimit() {
        return this.range === 'page' ? 604 : 30
      },

      surahName() {
        if (!this.loading && this.chapters.length > 0 && this.verses.length > 0 && this.verses[this.activeVerse]) {
          const surah = this.chapters.find(s => s.id === this.verses[this.activeVerse].surah_id);
          return surah ? surah.name : this.t('loading');
        }
        return this.t('loading');
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
          surahBorder.style.backgroundImage = 'url("./assets/Surah-border-light.svg")';
        } else {
          root.removeAttribute('data-theme');
          surahBorder.style.backgroundImage = 'url("./assets/Surah-border-dark.svg")'

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
        this.locale = lang;
        
        // Update toast notifications RTL
        const toastContainers = document.querySelectorAll('.Vue-Toastification__container');
        toastContainers.forEach(container => {
          if (lang === 'ar') {
            container.style.direction = 'rtl';
            container.style.textAlign = 'right';
          } else {
            container.style.direction = 'ltr';
            container.style.textAlign = 'left';
          }
        });
        
        try {localStorage.setItem('language', lang); } catch (e) { console.log(e) }
      },
      toggleLanguage() {
        const next = this.locale === 'ar' ? 'en' : 'ar';
        this.applyLanguage(next);
      },
      async fetchChapters() {
        this.loading = true;
        try {
          const response = await fetch(`${this.apiUrl}/surahs`);
          
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          this.chapters = await response.json();
        } catch (error) {
          console.error('Error fetching chapters:', error);
          
          let errorMessage = this.t('errors.fetchChaptersError');
          
          if (error.message.includes('Failed to fetch') || error instanceof TypeError) {
            errorMessage = this.t('errors.networkError');
          } else if (error.message.includes('HTTP error')) {
            errorMessage = this.t('errors.serverError');
          }
          
          // Use nextTick to avoid "unhandled error" warning
          await this.$nextTick();
          if (this.toast) {
            this.toast.error(errorMessage, {
              timeout: 5000,
              closeOnClick: true,
              pauseOnHover: true,
            });
          }
          
          this.loading = false;
        }
      },

      async fetchVerses() {
        this.loading = true;
        try {
          const { startChapter, startVerse, endChapter, endVerse } = this.verseRangeValue;
          const { start, end } = this.rangeValue;
          const params = new URLSearchParams({
            range_type: this.range,
            range_value: this.range === "key" ? `${startChapter}:${startVerse}-${endChapter}:${endVerse}` : `${start}:${end}`,
          }).toString();

          const response = await fetch(`${this.apiUrl}/verses?${params}`);
          
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          this.verses = await response.json();

          this.activeVerse = 0;
          this.loading = false;
          await this.$nextTick();
          this.restart();
        } catch (error) {
          console.error('Error fetching verses:', error);
          
          let errorMessage = this.t('errors.fetchVersesError');
          
          if (error.message.includes('Failed to fetch') || error instanceof TypeError) {
            errorMessage = this.t('errors.networkError');
          } else if (error.message.includes('HTTP error')) {
            errorMessage = this.t('errors.serverError');
          }
          
          // Use nextTick to avoid "unhandled error" warning
          await this.$nextTick();
          if (this.toast) {
            this.toast.error(errorMessage, {
              timeout: 5000,
              closeOnClick: true,
              pauseOnHover: true,
            });
          }
          
          this.loading = false;
        }
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

      async fetchVisitCount() {
        try {
          const response = await fetch('https://abacus.jasoncameron.dev/hit/quranlink.app/visits', { cache: 'no-store' });
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          const json = await response.json();
          if (json && typeof json.value !== 'undefined') {
            this.visitCount = json.value;
          }
        } catch (err) {
          console.error('Error fetching visit count:', err);
          this.visitCount = null;
        }
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
      this.fetchVisitCount();
    },
    beforeUnmount() {
      window.removeEventListener('keydown', this.onEscKey);
    },
  }
</script>
