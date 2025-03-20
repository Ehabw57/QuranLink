 <template>
  <h4> Mode = {{ mode }} : Range = {{ range }}</h4>
  <h5>range = {{value}} </h5>
  <h5>rangever = {{VV}} </h5>
  <TestConfig 
  v-model:mode="mode"
  v-model:range="range"
  :modeOptions='modeOptions'
  :rangeOptions='rangeOptions'/>
  <VerseSelector v-if="range === 'verse'" :chapters="chapters" v-model="VV" />
  <RangeSelector v-else v-model="value" :limit="limits"/>
</template>

<script>
import TestConfig from './TestConfig.vue';
import RangeSelector from './RangeSelector.vue';
import VerseSelector from './VerseSelector.vue';

export default {
  components: {VerseSelector, TestConfig , RangeSelector}, 
  data() {
    return {
      mode: 'words',
      range:'juz', 
      modeOptions: ['words', 'pages', 'verses'],
      rangeOptions: ['juz', 'page', 'verse'],
      chapters: [{"id":1,"name":"الفاتحة","en_name":"Al-Fatihah","ayahs_count":7},{"id":2,"name":"البقرة","en_name":"Al-Baqarah","ayahs_count":286},{"id":3,"name":"آل عمران","en_name":"Ali 'Imran","ayahs_count":200},{"id":4,"name":"النساء","en_name":"An-Nisa","ayahs_count":176},{"id":5,"name":"المائدة","en_name":"Al-Ma'idah","ayahs_count":120},{"id":6,"name":"الأنعام","en_name":"Al-An'am","ayahs_count":165},{"id":7,"name":"الأعراف","en_name":"Al-A'raf","ayahs_count":206},{"id":8,"name":"الأنفال","en_name":"Al-Anfal","ayahs_count":75},{"id":9,"name":"التوبة","en_name":"At-Tawbah","ayahs_count":129},{"id":10,"name":"يونس","en_name":"Yunus","ayahs_count":109},{"id":11,"name":"هود","en_name":"Hud","ayahs_count":123},{"id":12,"name":"يوسف","en_name":"Yusuf","ayahs_count":111},{"id":13,"name":"الرعد","en_name":"Ar-Ra'd","ayahs_count":43},{"id":14,"name":"ابراهيم","en_name":"Ibrahim","ayahs_count":52},{"id":15,"name":"الحجر","en_name":"Al-Hijr","ayahs_count":99},{"id":16,"name":"النحل","en_name":"An-Nahl","ayahs_count":128},{"id":17,"name":"الإسراء","en_name":"Al-Isra","ayahs_count":111},{"id":18,"name":"الكهف","en_name":"Al-Kahf","ayahs_count":110},{"id":19,"name":"مريم","en_name":"Maryam","ayahs_count":98},{"id":20,"name":"طه","en_name":"Taha","ayahs_count":135},{"id":21,"name":"الأنبياء","en_name":"Al-Anbya","ayahs_count":112},{"id":22,"name":"الحج","en_name":"Al-Hajj","ayahs_count":78}],
      value: {start: 1, end: 1},
      VV: {startChapter: 1, endChapter:1, startVerse:1, endVerse:1}
    };
  },
  computed: {
    limits () {
      if (this.range === 'page') {
        return 604;
      } else if (this.range === 'juz') {
        return 30;
      } else if (this.range === 'rub') {
        return 240;
      }
    return 0;
    }
  }
};
</script>



