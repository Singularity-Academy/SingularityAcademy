<script setup lang="ts">
import { ref, h } from "vue"
import { RouterLink } from "vue-router"
import {
  NLayoutHeader,
  NIcon,
  NButton,
  NDropdown,
  NText
} from "naive-ui"
import {
  IconMoon,
  IconSun,
  IconMenu
} from "#components"

import { navMenuOptions } from '~/router/nav'

defineProps<{ darkMode: boolean }>()
const emit = defineEmits(["toggle-dark"])

const { locale, setLocale, t } = useI18n()
const dropdownVisible = ref(false)
const languageDropdownVisible = ref(false)

const toggleDarkMode = () => {
  emit("toggle-dark")
}

const menuOptions = navMenuOptions.map(item => ({
  label: () => h(RouterLink, { to: item.to }, { default: () => t(item.label) }),
  key: item.key,
  icon: () => h(NIcon, null, { default: () => h(item.icon) })
}))

const languageOptions = [
  { label: 'English', value: 'en' },
  { label: '简体中文', value: 'zh' },
  { label: 'Español', value: 'es' },
  { label: 'Français', value: 'fr' },
  { label: 'Deutsch', value: 'de' },
  { label: '日本語', value: 'ja' },
  { label: 'العربية', value: 'ar' }
]

const handleLanguageChange = (value: typeof locale.value) => {
  setLocale(value)
  languageDropdownVisible.value = false
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
      <RouterLink to="/auth/login">
        <NButton text class="nav-item">{{ t('common.signIn') }}</NButton>
      </RouterLink>
      <RouterLink to="/auth/register">
        <NButton text class="nav-item">{{ t('common.signUp') }}</NButton>
      </RouterLink>
      <NButton text circle @click="toggleDarkMode" class="nav-item"
        :title="darkMode ? t('Navbar.lightMode') : t('Navbar.darkMode')">
        <NIcon>
          <component :is="darkMode ? IconSun : IconMoon" />
        </NIcon>
      </NButton>
      <n-dropdown trigger="click" :options="languageOptions" key-field="value" label-field="label"
        :show="languageDropdownVisible" placement="bottom-end" @select="handleLanguageChange"
        @clickoutside="languageDropdownVisible = false">
        <NButton quaternary class="nav-item lang-switch" @click="languageDropdownVisible = !languageDropdownVisible">
          {{languageOptions.find(lang => lang.value === locale)?.label}}
        </NButton>
      </n-dropdown>
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