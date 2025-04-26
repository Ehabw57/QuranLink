<template>
  <div class="border-image"></div>
  <div class="surahName">{{ surahName }}</div>
</template>

<script>
export default {
  props: {
    surahName: {
      type: String,
      required: true
    }
  }
}
</script>
