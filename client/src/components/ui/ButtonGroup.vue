.template>
<template>
    <div class="button-group" :class="{ tabed: tabed }">
        <button
            v-for="opt in options"
            :key="opt && (opt.name || opt)"
            :class="{ active: modelValue === (opt.name || opt), tabbed: tabed, selected: modelValue === (opt.name || opt) }"
            @click="$emit('update:modelValue', opt.name || opt)"
        >
            <component v-if="getIcon(opt)" :is="getIcon(opt)" class="btn-icon" />
            <span class="btn-label">{{ getLabel(opt) }}</span>
        </button>
    </div>
</template>

<script>
import { useLanguage } from '@/composables/useLanguage';

export default {
    name: 'ButtonGroup',
    props: {
        // options: array of strings or { name: string, icon?: Component }
        options: { type: Array, required: true },
        modelValue: { type: String, required: true },
        labelPrefix: { type: String, default: '' }, // e.g., 'modes' or 'ranges'
        tabed: { type: Boolean, default: false },
    },
    emits: ['update:modelValue'],
    setup(props) {
        const { t, te } = useLanguage();

        const getLabel = (item) => {
            const name = typeof item === 'string' ? item : item.name;
            if (props.labelPrefix) {
                const key = `${props.labelPrefix}.${name}`;
                if (te(key)) return t(key);
            }
            return name;
        };

        const getIcon = (item) => {
            if (!item) return null;
            if (typeof item === 'string') return null;
            return item.icon || null;
        };

        return { getLabel, getIcon };
    },
};
</script>

<style scoped>
.button-group {
    display: inline-flex;
    gap: 6px;
    align-items: center;
}

button {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
    transition: background 120ms ease, transform 120ms ease;
}

button.tabbed {
    padding: 6px 6px;
}

button.active {
    color: var(--color-active);
}

button.active.tabbed {
    border-bottom: 2px solid var(--color-active);
}

.btn-icon {
    width: 18px;
    height: 18px;
}

</style>

