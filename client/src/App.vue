<template>
  <div class="config">
    <ButtonOptions :options="modes" v-model="mode" />
    <div class="seprator"></div>
    <ButtonOptions :options="ranges" v-model="range" />
    <div class="seprator"></div>
    <VerseSelector v-if="range=='key'" :chapters="chapters" v-model="verseRangeValue" />
    <RangeSelector :limit='rangeLimit' v-else v-model="rangeValue"/>
    <div class="seprator"></div>
    <input type="checkbox" v-model="isRepeate" id="repeate">
    <label for="repeate">repeate</label>
    <button @click="shuffleVerses">random</button>
  </div>


  <div class="border-container">
    <SurahBorder :surahName="surahName.name" />
  </div>


  <div class="test-container" v-if="!loading && verses[verseIndex]">

    <div class="verses-test" v-if="mode === 'verses'">
    <testVerse  ref="verseTest" v-model="surahId" @done="handelDone" :verses="oriVerses" />
    </div>

    <div class="words-test" v-else >
      <testWord  ref="wordsTest" v-model="surahId" @done="handelDone"  :verse="verses[verseIndex]" />
    </div>

  </div>

  <div v-else>
    <h2>still loading...</h2>
  </div>


  <div>
    <button @click="skip">skip</button>
    <button @click="hint">hint</button>
    <button @click="restart">restart</button>
    <button @click="skipQustion">skipQuestion</button>
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
        verseIndex: 0,
        surahId: 1,
        isRepeate: false,
        modes: ['words', 'verses'],
        mode: 'words',
        ranges: ['juz', 'page', 'key'],
        range: 'page',
        rangeLimit: 604,
        rangeValue: {start: 1, end:1},
        verseRangeValue: {sc: 1, sv: 1, ec: 1, ev: 7},
        loading: true
      }
    },
    computed: {
      surahName() {
        if (this.chapters.length > 0) {
          return this.chapters.find(s => s.id === this.surahId)
        }
        //if chapters still didnt load
        return { name: "الفاتحة" };
      },

      oriVerses() {
        return this.verses.slice(this.verseIndex)
      }
    },

    methods: {
      async fetchChapters() {
        this.loading = true;
        const response = await fetch("http://localhost:8000/surahs");
        this.chapters = await response.json();
        this.loading = false;
      },

      async fetchVerses() {
        const { sc, sv, ec, ev } = this.verseRangeValue;
        const { start, end } = this.rangeValue;
        const params = new URLSearchParams({
          range_type: this.range,
          range_value: this.range === "key" ? `${sc}:${sv}-${ec}:${ev}` : `${start}:${end}`,
        }).toString();
        this.loading = true;
        const response = await fetch(`http://localhost:8000/verses?${params}`);
        this.verses = await response.json();
        this.loading = false;
      },

      pairVerses() {
        const chunks = [];
        for (let i = 0; i < this.verses.length; i++) {
          if (this.verses[i + 1]) {
          chunks.push([this.verses[i], this.verses[i + 1]]);
          }
        }
        this.versesChunks = chunks;
        return chunks;
      },

      shuffleVerses() {
        this.versesChunks = this.versesChunks.slice(this.currentChunk);
        this.versesChunks = this.store.shuffleArray(this.versesChunks);
        this.verseIndex = this.randomIndex(this.verses.length - 1);
      },
      delay(ms) {
        return new Promise(reslove => setTimeout(reslove, ms))
      },

      async handelDone() {
        if (this.mode === 'words') {
          if (!this.isRepeate) {
            await this.delay(700); 
            this.verseIndex = (this.verseIndex + 1) % this.verses.length;
          }
          this.$refs.wordsTest.restartTest();
        } else {
          if (!this.isRepeate) {
            this.currentChunk = (this.currentChunk + 1) % this.versesChunks.length;
          }
          this.$refs.verseTest.restartTest();
        }
      },

      randomIndex(max) {
        return Math.floor(Math.random() * max)
      },

      restart(){
        this.mode === 'words' ? this.$refs.wordsTest.restartTest() : this.$refs.verseTest.restartTest()
      },
      skip() {
        this.store.currentInput.emitCorrect()
      },
      skipQustion(){
        this.handelDone();
      },
      hint() {
        this.store.currentInput.addHint()
      },
    },

    watch: {
      range(newValue) {
        const limits = {
          juz: 30,
          page: 604,
        };
        this.rangeLimit = limits[newValue] || 0;
      },

      rangeValue: {
        async handler() {
          await this.fetchVerses();
          this.currentChunk = 0;
          this.verseIndex = 0;
          this.pairVerses();
        },
        deep: true
      },
      verseRangeValue: {
        async handler() {
          await this.fetchVerses();
          this.currentChunk = 0;
          this.verseIndex = 0;
          this.pairVerses();
        },
        deep: true
      }
    },
    async created() {
      await this.fetchChapters()
      await this.fetchVerses()
      this.pairVerses()
    }
  }
</script>
