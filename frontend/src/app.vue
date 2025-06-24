<script setup lang="ts">
import NavBar from "~/components/nav-bar.vue"
import MainContent from "~/components/main-content.vue"
import "~/styles/global.scss"

import { ref } from "vue"
import { darkTheme, lightTheme } from "naive-ui"

const darkMode = ref(false)

const theme = computed(() => (darkMode.value ? darkTheme : lightTheme))

const toggleDark = () => {
  darkMode.value = !darkMode.value
}
</script>

<template>
  <n-config-provider :theme="theme">
    <n-global-style />
    <n-message-provider>
      <n-dialog-provider>
        <n-layout class="main-layout">
          <NavBar :dark-mode="darkMode" @toggle-dark="toggleDark" />
          <MainContent />
        </n-layout>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>
