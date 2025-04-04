<template>
  <div>
    <ButtonOptions :options="modes" v-model="mode" />
    <label>||</label>
    <ButtonOptions :options="ranges" v-model="range" />
    <label>||</label>
    <VerseSelector v-if="range=='key'" :chapters="chapters" v-model="verseRangeValue" />
    <RangeSelector :limit='40' v-else v-model="rangeValue"/>
    <input @change="handelRandom" type="checkbox" v-model="isRandom" id="random">
    <label for="random">random</label>
  </div>

  <div>
    <SurahBorder :surahName="surahName.name" />
  </div>

  <div v-if="!loading && verses[verseIndex]">
    <div v-if="mode === 'verses'">
    <testVerse  ref="verseTest" v-model="surahId" @done="handelDone" :oriVerses="versesChunks[currentChunk]" />
    </div>
    <testWord v-else ref="wordsTest" v-model="surahId" @done="handelDone"  :verse="verses[verseIndex]" />
  </div>

  <div v-else>
    <h2>still loading...</h2>
  </div>


  <div>
    <button @click="skip">skip</button>
    <button @click="hint">hint</button>
    <button @click="restart">restart</button>
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
        versesChunks:[],
        currentChunk: 0,
        verseIndex: 0,
        surahId: 1,
        isRandom: false,
        modes: ['words', 'verses'],
        mode: 'words',
        ranges: ['juz', 'page', 'key'],
        range: 'key',
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
      return { name: "الفاتحه" };
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

      chunkVerses(size) {
        const chunks = [];
        for (let i = 0; i < this.verses.length; i += size) {
          chunks.push(this.verses.slice(i, i + size));
        }
        this.versesChunks = chunks;
        return chunks;
      },
      handelRandom() {
        this.currentChunk = 0;
        if(this.isRandom) {
          this.versesChunks = this.store.shuffleArray(this.versesChunks)
        } else {
          this.chunkVerses(5);
        }
      },

      handelDone() {
        if (this.mode == 'words') {
          this.verseIndex++;
          this.$refs.wordsTest.restartTest()
        } else {
          this.currentChunk++;
        }
      },
      randomVerseIndex(max) {
        return Math.floor(Math.random() * max)
      },
      restart(){
        this.mode === 'words' ? this.$refs.wordsTest.restartTest() : this.$refs.verseTest.restartTest()
      },
      skip() {
        this.store.currentInput.emitCorrect()
      },
      hint() {
        this.store.currentInput.addHint()
      },
    },
    watch: {
      rangeValue: {
        async handler() {
          await this.fetchVerses();
          this.chunkVerses(5);
        },
        deep: true,
      },
      verseRangeValue: {
        async handler() {
          await this.fetchVerses();
          this.chunkVerses(5);
        },
        deep: true
      }
    },
    async created() {
      await this.fetchChapters()
      await this.fetchVerses()
      this.chunkVerses(5)
    }
  }
</script>
<style scoped>
div.conot {
  display: flex;
  justify-content: center;
  flex-direction: row-reverse;
}
</style>
