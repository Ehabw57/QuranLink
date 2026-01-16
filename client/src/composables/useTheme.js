import { ref } from 'vue';

export function useTheme() {
  const theme = ref('dark');
  
  const applyTheme = (newTheme) => {
    const root = document.documentElement;
    
    if (newTheme === 'light') {
      root.setAttribute('data-theme', 'light');
    } else {
      root.removeAttribute('data-theme');
    }
    
    theme.value = newTheme;
    
    try {
      localStorage.setItem('theme', newTheme);
    } catch (e) {
      console.warn('Could not save theme to localStorage:', e);
    }
  };
  
  const toggleTheme = () => {
    applyTheme(theme.value === 'light' ? 'dark' : 'light');
  };
  
  const initTheme = () => {
    let initial = 'dark';
    try {
      const saved = localStorage.getItem('theme');
      if (saved === 'light' || saved === 'dark') {
        initial = saved;
      } else if (window.matchMedia?.('(prefers-color-scheme: light)').matches) {
        initial = 'light';
      }
    } catch (e) {
      console.warn('Could not read theme from localStorage:', e);
    }
    applyTheme(initial);
  };
  
  return {
    theme,
    applyTheme,
    toggleTheme,
    initTheme,
  };
}
