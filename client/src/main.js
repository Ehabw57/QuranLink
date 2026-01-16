import { createApp } from 'vue';
import App from './App.vue';
import i18n from './i18n';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import '@/assets/styles/main.css';

const app = createApp(App);

const toastOptions = {
  position: 'bottom-right',
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false,
};

app
  .use(i18n)
  .use(Toast, toastOptions)
  .mount('#app');
