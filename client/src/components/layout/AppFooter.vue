<template>
  <footer class="site-footer">
    <div class="footer-content">
      <div class="footer-about">
        <SiteBrand compact />
        <p>{{ t('footer.about') }}</p>
        <div class="footer-visits" v-if="visitCount !== null" aria-hidden="false" title="Visits">
          <Eye />
          <span class="visit-count">{{ visitCount }}</span>
        </div>
      </div>
      <div class="footer-social">
        <div class="social-links">
          <a 
            v-for="link in socialLinks" 
            :key="link.url" 
            :href="link.url" 
            target="_blank" 
            rel="noopener noreferrer" 
            :aria-label="link.label"
          >
            <component :is="link.icon" />
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useLanguage } from '@/composables/useLanguage';
import SiteBrand from './SiteBrand.vue';
import { Eye, Github, GitBranch, Linkedin, Globe, Youtube } from 'lucide-vue-next';

export default {
  name: 'AppFooter',
  components: { SiteBrand, Eye, Github, GitBranch, Linkedin, Globe, Youtube },
  setup() {
    const { t } = useLanguage();
    const visitCount = ref(null);
    
    const socialLinks = [
      { url: 'https://github.com/Ehabw57', icon: Github, label: 'GitHub' },
      { url: 'https://github.com/Ehabw57/QuranLink/', icon: GitBranch, label: 'Repository' },
      { url: 'https://www.linkedin.com/in/ehababdelrady', icon: Linkedin, label: 'LinkedIn' },
      { url: 'https://ehabw57.github.io/personal_portofolio/', icon: Globe, label: 'Portfolio' },
      { url: 'https://www.youtube.com/@mercy_world57', icon: Youtube, label: 'YouTube' },
    ];
    
    const fetchVisitCount = async () => {
      try {
        const response = await fetch('https://abacus.jasoncameron.dev/hit/quranlink.app/visits', { cache: 'no-store' });
        if (!response.ok) throw new Error('Failed to fetch');
        const json = await response.json();
        visitCount.value = json?.value ?? null;
      } catch {
        visitCount.value = null;
      }
    };
    
    onMounted(fetchVisitCount);
    
    return { t, visitCount, socialLinks };
  },
};
</script>
