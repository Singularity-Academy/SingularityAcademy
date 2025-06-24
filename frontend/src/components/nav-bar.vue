<script setup lang="ts">
import '~/styles/theme.scss'
import { ref, h } from 'vue'
import { RouterLink } from 'vue-router'
import {
  NLayoutHeader,
  NIcon,
  NButton,
  NDropdown,
  NText
} from 'naive-ui'

import {
  IconHouse,
  IconLayoutDashboard,
  IconMoon,
  IconSun,
  IconMenu
} from '#components'

const darkMode = ref(false)
const dropdownVisible = ref(false)

const toggleDarkMode = () => {
  darkMode.value = !darkMode.value
  const cls = document.documentElement.classList
  darkMode.value ? cls.add('dark') : cls.remove('dark')
}

const menuOptions = [
  {
    label: () => h(RouterLink, { to: '/' }, { default: () => '首页' }),
    key: 'home',
    icon: renderIcon(IconHouse)
  },
  {
    label: () => h(RouterLink, { to: '/dashboard' }, { default: () => '仪表盘' }),
    key: 'dashboard',
    icon: renderIcon(IconLayoutDashboard)
  }
]

function renderIcon(icon: any) {
  return () => h(NIcon, null, { default: () => h(icon) })
}
</script>

<template>
  <n-layout-header class="nav-bar">
    <div class="left">
      <RouterLink to="/" class="logo">
        <NText strong class="logo-text">SingulariyAcademy</NText>
      </RouterLink>
    </div>
    <div class="right">
      <NButton text class="nav-item">登录</NButton>
      <NButton text circle @click="toggleDarkMode" class="nav-item">
        <NIcon>
          <component :is="darkMode ? IconSun : IconMoon" />
        </NIcon>
      </NButton>
      <NButton quaternary class="nav-item lang-switch">中文(简体)</NButton>
      <n-dropdown trigger="click" :options="menuOptions" placement="bottom-end" :show="dropdownVisible"
        @clickoutside="dropdownVisible = false" @select="dropdownVisible = false">
        <NButton quaternary circle @click="dropdownVisible = !dropdownVisible">
          <NIcon>
            <IconMenu />
          </NIcon>
        </NButton>
      </n-dropdown>
    </div>
  </n-layout-header>
</template>

<style scoped lang="scss">
.nav-bar {
  height: 4rem;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--sider-bg);
  border-bottom: 1px solid var(--divider-color);
  box-sizing: border-box;
  position: sticky;
  top: 0;
  z-index: 100;
}

.left .logo {
  text-decoration: none;
  display: flex;
  align-items: center;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: bold;
  color: var(--text-color);
}

.right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-item {
  font-weight: 500;
  color: var(--text-color);
}

.lang-switch {
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  background-color: var(--hover-bg);
  color: var(--text-color);
}
</style>
