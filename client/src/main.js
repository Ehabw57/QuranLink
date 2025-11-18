import { createApp } from 'vue'
import App from './App.vue'
import i18n from './i18n'
import Toast from "vue-toastification"
import "vue-toastification/dist/index.css"

import ButtonOptions from './components/ButtonOptions.vue'
import RangeSelector from './components/RangeSelector.vue'
import VerseSelector from './components/VerseSelector.vue'
import SurahBorder from './components/SurahBorder.vue'
import inputBox from './components/inputBox.vue'
import testVerse from './components/testVerse.vue'
import testWord from './components/testWord.vue'

const app = createApp(App)

const toastOptions = {
  position: "bottom-right",
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: "button",
  icon: true,
  rtl: false
}

app
  .use(i18n)
  .use(Toast, toastOptions)
  .component('ButtonOptions', ButtonOptions)
  .component('RangeSelector', RangeSelector)
  .component('VerseSelector', VerseSelector)
  .component('SurahBorder', SurahBorder)
  .component('inputBox', inputBox)
  .component('testVerse', testVerse)
  .component('testWord', testWord)
  .mount('#app')

