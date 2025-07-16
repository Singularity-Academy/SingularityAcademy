<script setup lang="ts">
import { ref, computed } from 'vue'
import NavBar from '~/components/nav-bar.vue'
import MainContent from '~/components/main-content.vue'
import Footer from '~/components/footer.vue'
import '~/styles/global.scss'
import { darkTheme } from 'naive-ui'
import {useThemeStore} from "~/stores/theme";
const darkMode = ref(false)

const themeStore = useThemeStore()

const theme = computed(() => (themeStore.actualTheme === 'dark' ? darkTheme : null))
</script>

<template>
  <title>Singularity Academy</title>
  <n-config-provider :theme="theme">
    <n-global-style />
    <n-message-provider>
      <n-dialog-provider>
        <n-layout class="main-layout">
          <NavBar :dark-mode="darkMode" @toggle-dark="themeStore.toggleTheme()" />
          <MainContent />
          <Footer />
        </n-layout>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>
