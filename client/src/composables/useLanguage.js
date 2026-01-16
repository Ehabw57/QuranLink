import { useI18n } from 'vue-i18n';

export function useLanguage() {
  const { locale, t, te } = useI18n();
  
  const applyLanguage = (lang) => {
    const root = document.documentElement;
    const dir = lang === 'ar' ? 'rtl' : 'ltr';
    
    root.setAttribute('lang', lang);
    root.setAttribute('dir', dir);
    locale.value = lang;
    
    // Update toast notifications RTL
    const toastContainers = document.querySelectorAll('.Vue-Toastification__container');
    toastContainers.forEach(container => {
      container.style.direction = dir;
      container.style.textAlign = lang === 'ar' ? 'right' : 'left';
    });
    
    try {
      localStorage.setItem('language', lang);
    } catch (e) {
      console.warn('Could not save language to localStorage:', e);
    }
  };
  
  const toggleLanguage = () => {
    applyLanguage(locale.value === 'ar' ? 'en' : 'ar');
  };
  
  const initLanguage = () => {
    let initial = 'en';
    try {
      const saved = localStorage.getItem('language');
      if (saved === 'ar' || saved === 'en') {
        initial = saved;
      }
    } catch (e) {
      console.warn('Could not read language from localStorage:', e);
    }
    applyLanguage(initial);
  };
  
  return {
    locale,
    t,
    te,
    applyLanguage,
    toggleLanguage,
    initLanguage,
  };
}
