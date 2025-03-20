<template>
  <div class="image-container">
    <img src="../assets/Surah-border.svg" alt="Surah Border">
    <div class="text-overlay">{{ surahName }}</div>
  </div>
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

<style scoped>
  @font-face {
    font-family: 'SurahName';
    src: url('../assets/fonts/SurahNames.woff') format('woff');
    font-weight: normal;
    font-style: normal;
  }

  .image-container {
    position: relative;
    display: inline-block;
    width: 100%;  
    max-width: 21em; 
  }

  .image-container img {
    width: 100%; 
    height: auto;
  }

  .text-overlay {
    position: absolute;
    font-family: 'SurahName', sans-serif;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: black;
    font-size: 1.8em;
    text-align: center;
  }
</style>

