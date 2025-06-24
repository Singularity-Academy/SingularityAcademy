<script setup lang="ts">
import NavBar from "~/components/nav-bar.vue"
import MainContent from "~/components/main-content.vue"
import "~/styles/global.scss"
</script>

<template>
  <n-config-provider>
    <n-global-style />
    <n-message-provider>
      <n-dialog-provider>
        <n-layout class="main-layout">
          <nav-bar />
          <n-layout-content class="main-content">
            <main-content />
          </n-layout-content>
        </n-layout>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>
