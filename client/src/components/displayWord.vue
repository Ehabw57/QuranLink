<template>
  <p class="quran-text">
  <slot/>
  </p>
</template>

<style scoped>
@font-face {
  font-family: "Uthmani";
  src: url('../assets/fonts/Uthmanic.woff') format('woff');
}

p.quran-text {
  font-family: "Uthmani";
  display: inline-block;
  margin: 0 2px;
  font-size: 13px;
}
</style>
