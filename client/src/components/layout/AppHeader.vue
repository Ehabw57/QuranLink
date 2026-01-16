<template>
    <header class="site-header">
        <SiteBrand />
        <div class="mode-select">
            <ButtonGroup :tabed="true" :options="modeOptions" :modelValue="mode" @update:modelValue="onModeChange"
                labelPrefix="modes" />
        </div>
        <div>
        <button class="lang-toggle" @click="toggleLanguage">
            <Languages />
        </button>
        <button class="icon-btn" @click="toggleTheme" :aria-label="'Toggle theme'">
            <component :is="theme === 'dark' ? Sun : Moon" />
        </button>
        <button class="settings" @click="$emit('openSettings')" :aria-label="t('header.settings')">
            <Settings />
        </button>
        </div>  
    </header>
</template>

<script>
import { useTheme } from '@/composables/useTheme';
import { useLanguage } from '@/composables/useLanguage';
import SiteBrand from './SiteBrand.vue';
import ButtonGroup from '@/components/ui/ButtonGroup.vue';
import { Sun, Moon, Settings, Languages } from 'lucide-vue-next';

export default {
    name: 'AppHeader',
    components: { SiteBrand, ButtonGroup, Sun, Moon, Settings, Languages },
    props: {
        mode: { type: String, required: true },
    },
    emits: ['openSettings', 'update:mode'],
    setup(props, { emit }) {
        const { theme, toggleTheme } = useTheme();
        const { locale, t, toggleLanguage } = useLanguage();
        const modeOptions = ['words', 'verses'];

        const onModeChange = (val) => emit('update:mode', val);

        return { theme, toggleTheme, locale, t, toggleLanguage, modeOptions, onModeChange, Sun, Moon, Settings, Languages };
    },
};
</script>

<style>
    .settings {
        display: inline-flex;
    }

    @media (min-width: 900px) {
        .settings {
            display: none;
        }
    }
</style>
