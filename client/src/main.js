import { createApp } from 'vue'
import App from './App.vue'

import ButtonOptions from './components/ButtonOptions.vue'
import RangeSelector from './components/RangeSelector.vue'
import VerseSelector from './components/VerseSelector.vue'
import SurahBorder from './components/SurahBorder.vue'
import displayWord from './components/displayWord.vue'
import inputBox from './components/inputBox.vue'
import testVerse from './components/testVerse.vue'
import testWord from './components/testWord.vue'

const app = createApp(App)

app
  .component('ButtonOptions', ButtonOptions)
  .component('RangeSelector', RangeSelector)
  .component('VerseSelector', VerseSelector)
  .component('SurahBorder', SurahBorder)
  .component('displayWord', displayWord)
  .component('inputBox', inputBox)
  .component('testVerse', testVerse)
  .component('testWord', testWord)
  .mount('#app')

