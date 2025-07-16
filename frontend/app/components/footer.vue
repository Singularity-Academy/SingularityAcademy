<script setup lang="ts">
import { NText, NFlex, NButton } from 'naive-ui'

const currentYear = new Date().getFullYear()

const chrisLinks = [
  { name: 'ClickMood', url: 'http://clickmood.krymusic.top/' },
  { name: 'Studio', url: 'http://studio.krypoto.top/' },
  { name: 'Photography', url: 'http://photograph.krypoto.top/' },
  { name: 'Blog', url: 'https://chrisdsasa.github.io/' },
  { name: 'Twitter', url: 'https://x.com/KrypotoZ' }
]
</script>

<template>
  <div class="footer-wrapper">
    <div class="gradient-bar" />

    <n-flex justify="space-between" align="center" class="footer-main">
      <n-flex direction="column" class="footer-left">
        <n-text class="footer-title">Creative Universe Suggestions</n-text>
        <n-text class="footer-desc" style="margin-top: 0.5rem;">
          Exploring the intersection of technology and creativity. Join me on these platforms to stay
          connected.
        </n-text>
      </n-flex>

      <n-flex gap="12" wrap class="footer-right">
        <n-button
          v-for="(link, index) in chrisLinks"
          :key="index"
          :tag="'a'"
          :href="link.url"
          target="_blank"
          rel="noopener noreferrer"
          quaternary
          class="footer-button"
          :title="link.name"
        >
          {{ link.name }}
        </n-button>
      </n-flex>
    </n-flex>

    <n-flex vertical align="center" justify="center" class="footer-note">
      <n-text class="footer-copy">
        © {{ currentYear }} 2025 AI Online School. Crafted with ❤️ by KRYPOTO TeaM.
        <br />
        Thanks for contributors' commitment for accessible education worldwide.
      </n-text>
    </n-flex>
  </div>
</template>

<style scoped lang="scss">
.footer-wrapper {
  position: relative;
  border-top: 1px solid var(--divider-color);
  padding: 4rem 0;
  background: linear-gradient(to top, var(--hover-bg), var(--main-bg));
}

.gradient-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(to right, #60a5fa, #a78bfa);
  animation: gradientFlow 3s ease infinite;
}

.footer-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  width: 100%;
}

.footer-left {
  max-width: 50%;
}

.footer-title {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(to right, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
  display: inline-block;
}

.footer-desc {
  font-size: 1rem;
  color: var(--text-color);
  opacity: 0.75;
  line-height: 1.75;
  max-width: 400px;
}

.footer-right {
  max-width: 45%;
  flex-wrap: nowrap;
  justify-content: flex-end;
  gap: 12px;
}

.footer-button {
  min-width: 80px;
  padding: 0 1rem;
  font-weight: 500;
  color: #3b82f6;
  background-color: transparent;
  border: 1px solid transparent;
  transition: all 0.2s ease;
}

.footer-button:hover {
  background-color: var(--hover-bg);
  border-color: #60a5fa;
  color: #2563eb;
}

.footer-note {
  margin-top: 3rem;
  text-align: center;
}

.footer-copy {
  font-size: 0.875rem;
  color: var(--text-color);
  opacity: 0.65;
  line-height: 1.75;
  max-width: 600px;
  text-align: center;
  margin: 0 auto;
}

@keyframes gradientFlow {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@media (max-width: 768px) {
  .footer-main {
    flex-direction: column;
    gap: 2rem;
  }
  .footer-left,
  .footer-right {
    max-width: 100%;
    justify-content: center !important;
  }
  .footer-right {
    flex-wrap: wrap;
  }
  .footer-button {
    min-width: auto;
    padding: 0.5rem 1rem;
  }
}
</style>
