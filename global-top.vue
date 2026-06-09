<script setup>
import logo from './assets/pg-logo.png'
</script>

<template>
  <div class="pg-fade"></div>
  <footer class="pg-footer">
    <img :src="logo" alt="Playground Tech" />
    <span>Playground Tech</span>
  </footer>
</template>

<style scoped>
/* safeguard: a soft band in the slide's background colour that keeps the
   footer legible even if a dense slide's content reaches the bottom edge */
.pg-fade {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 58px;
  background: linear-gradient(to top, var(--bg) 42%, transparent);
  z-index: 15;
  pointer-events: none;
}
.pg-footer {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.85rem 1.6rem;
  z-index: 20;
  pointer-events: none;
}
.pg-footer img {
  height: 18px;
  width: auto;
  display: block;
}
.pg-footer span {
  font-family: 'Hanken Grotesk', sans-serif;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: rgba(31, 42, 61, 0.5);
}
</style>
