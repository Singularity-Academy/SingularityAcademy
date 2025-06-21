<script setup lang="ts">
import NavBar from "~/components/nav-bar.vue";
</script>

<template>

  <n-config-provider>
    <n-global-style />

    <n-message-provider>
      <n-dialog-provider>

        <n-layout class="min-h-screen">
          <n-layout-header>
            <nav-bar />
          </n-layout-header>

          <n-layout-content>
            <NuxtPage />
          </n-layout-content>

        </n-layout>

      </n-dialog-provider>
    </n-message-provider>

  </n-config-provider>

</template>
