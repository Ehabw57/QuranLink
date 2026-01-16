<template>
  <div v-show="modelValue" class="modal" @click.self="close">
    <div class="modal-content">
      <button class="close" @click="close" aria-label="Close">
        <X />
      </button>
      <h1 v-if="title">{{ title }}</h1>
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { onMounted, onUnmounted } from 'vue';
import { X } from 'lucide-vue-next';

export default {
  name: 'AppModal',
  components: { X },
  props: {
    modelValue: { type: Boolean, required: true },
    title: { type: String, default: '' },
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const close = () => emit('update:modelValue', false);

    const onEscKey = (e) => {
      if (e.key === 'Escape' && props.modelValue) close();
    };

    onMounted(() => window.addEventListener('keydown', onEscKey));
    onUnmounted(() => window.removeEventListener('keydown', onEscKey));

    return { close };
  },
};
</script>
