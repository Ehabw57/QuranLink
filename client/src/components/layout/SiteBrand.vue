<template>
    <div class="site-brand" :class="{ compact }">
        <div class="logo" aria-hidden="true">
            <svg viewBox="0 0 100 100" role="img" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                stroke="currentColor" stroke-linecap="round" stroke-width="6">
                <path d="M50 10 L85 30 L85 70 L50 90 L15 70 L15 30 Z" opacity="0.2"></path>
                <path d="M50 10 L85 30 M85 70 L50 90 M15 70 L15 30"></path>
                <path d="M30 40 L50 30 L70 40 L70 60 L50 70 L30 60 Z"></path>
                <circle cx="50" cy="50" fill="currentColor" r="3"></circle>
            </svg>
        </div>
        <div class="brand-text" :style="{ display: compact ? 'flex' : null }">
            <h1 v-if="!compact" class="brand-title">{{ t('app.title') }}</h1>
            <h3 v-else class="brand-title">{{ t('app.title') }}</h3>
            <small class="brand-tagline">{{ t('app.tagline') }}</small>
        </div>
    </div>
</template>

<script>
import { useLanguage } from '@/composables/useLanguage';

export default {
    name: 'SiteBrand',
    props: {
        compact: {
            type: Boolean,
            default: false,
        },
    },
    setup() {
        const { t } = useLanguage();
        return { t };
    },
};
</script>

<style scoped>
.site-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    color: var(--color-text);
}

.site-brand .logo {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-text);
    background-image: none;
}

.site-brand.compact .logo {
    width: 36px;
    height: 36px;
}

.site-brand .logo svg {
    width: 100%;
    height: 100%;
    display: block;
}

.brand-text {
    display: none;
    flex-direction: column;
    line-height: 1;
}

.brand-title {
    margin: 0;
    font-weight: 700;
    color: var(--color-text);
    font-size: 1.05rem;
}

.site-brand.compact .brand-title {
    font-size: 1rem;
    font-weight: 600;
}

.brand-tagline {
    margin-top: 2px;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--color-muted);
}

@media (min-width: 768px) {
    .site-brand .brand-text {
        display: flex;
    }
}
</style>
