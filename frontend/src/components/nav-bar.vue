<script setup lang="ts">
import { ref, watch, h } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import {
  NButton,
  NIcon,
  NMenu,
  NText,
  NLayoutSider,
  NLayout,
  type MenuOption
} from 'naive-ui'

import {
  IconHouse,
  IconLayoutDashboard,
  IconMoon,
  IconSun,
  IconMenu
} from "#components";

const route = useRoute()
const emit = defineEmits<{ (e: 'navigate'): void }>()

const darkMode = ref(false)
const activeKey = ref('')
const collapsed = ref(false)

const toggleDarkMode = () => {
  darkMode.value = !darkMode.value
  updateThemeClass(darkMode.value)
}

const updateThemeClass = (isDark: boolean) => {
  if (isDark) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

function getActiveKey(path: string): string {
  if (path === '/') return 'go-back-home'
  if (path.startsWith('/dashboard')) return 'go-to-dashboard'
  return ''
}

activeKey.value = getActiveKey(route.path)

function createRouterLink(path: string, label: string) {
  return () =>
    h(
      RouterLink,
      {
        to: { path },
        onClick: () => emit('navigate')
      },
      { default: () => label }
    )
}

const menuOptions: MenuOption[] = [
  {
    label: createRouterLink('/', '首页'),
    key: 'go-back-home',
    icon: renderIcon(IconHouse)
  },
  {
    label: createRouterLink('/dashboard', '仪表盘'),
    key: 'go-to-dashboard',
    icon: renderIcon(IconLayoutDashboard)
  }
]

watch(() => route.path, (newPath) => {
  activeKey.value = getActiveKey(newPath)
})

if (darkMode.value) {
  document.documentElement.classList.add('dark')
}

const toggleCollapse = () => {
  collapsed.value = !collapsed.value
}
</script>

<template>
  <NLayout has-sider embedded>
    <NLayoutSider bordered collapse-mode="width" :collapsed-width="64" :width="240" :collapsed="collapsed"
      @collapse="collapsed = true" @expand="collapsed = false" class="sider-container">
      <div class="sider-header">
        <div class="logo-link">
          <div class="logo-image">
            <IconHouse :size="24" />
          </div>
          <NText class="logo-text" :depth="1">Calrif AI 知澜</NText>
        </div>
        <NButton quaternary circle @click="toggleCollapse" class="collapse-btn">
          <NIcon>
            <IconMenu />
          </NIcon>
        </NButton>
      </div>

      <div class="menu-container" v-show="!collapsed">
        <NMenu :options="menuOptions" :value="activeKey" :collapsed="collapsed" :collapsed-width="64"
          :collapsed-icon-size="22" />
      </div>

      <div class="sider-footer" v-show="!collapsed">
        <div class="action-buttons">
          <NButton circle @click="toggleDarkMode" class="theme-toggle">
            <NIcon>
              <component :is="darkMode ? IconMoon : IconSun" />
            </NIcon>
          </NButton>
        </div>
        <div class="footer-text">
          <NText depth="3">© 2025 Calrif AI</NText>
        </div>
      </div>
    </NLayoutSider>

    <NLayout class="main-content">
      <router-view />
    </NLayout>
  </NLayout>
</template>

<style scoped lang="scss">
.sider-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--sider-bg);
  transition: all 0.3s ease;

  .sider-header {
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    border-bottom: 1px solid var(--divider-color);

    .logo-link {
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 12px;
      overflow: hidden;
    }

    .logo-image {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background-color: var(--primary-color-light);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;

      svg {
        color: var(--primary-color);
      }
    }

    .logo-text {
      font-size: 18px;
      font-weight: 700;
      color: var(--primary-color);
      white-space: nowrap;
      transition: opacity 0.3s, width 0.3s;
      overflow: hidden;

      .n-layout-sider-collapsed & {
        opacity: 0;
        width: 0;
      }
    }


    .collapse-btn {
      width: 36px;
      height: 36px;
      font-size: 18px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }


  .menu-container {
    flex: 1;
    overflow-y: auto;
    padding: 16px 12px;

    :deep(.n-menu) {
      .n-menu-item {
        border-radius: 8px;
        margin-bottom: 4px;
        height: 46px;
        transition: background-color 0.2s;

        &--selected {
          background-color: var(--primary-color-light);
          color: var(--primary-color);

          .n-menu-item-content__icon {
            color: var(--primary-color);
          }
        }

        &:hover:not(.n-menu-item--selected) {
          background-color: var(--hover-bg);
        }
      }
    }
  }

  .sider-footer {
    padding: 0 16px 16px;
    display: flex;
    flex-direction: column;
    align-items: center;

    .action-buttons {
      width: 100%;
      display: flex;
      justify-content: center;
      margin-bottom: 12px;

      .theme-toggle {
        width: 40px;
        height: 40px;
        font-size: 18px;
      }
    }

    .footer-text {
      text-align: center;
      font-size: 12px;
      padding-top: 8px;
      width: 100%;
      border-top: 1px solid var(--divider-color);
    }
  }
}

.main-content {
  height: 100vh;
  overflow: auto;
  background-color: #fff;
  padding: 24px;
}

@media (max-width: 768px) {
  .sider-container {
    :deep(.n-layout-sider-scroll-container) {
      overflow-x: hidden;
    }

    .sider-header {
      padding: 0 12px;
    }

    .sider-footer {
      padding: 0 12px 12px;
    }
  }
}
</style>

<style lang="scss">
:root {
  --sider-bg: #ececec;
  --divider-color: #f0f0f0;
  --primary-color: #4e6fff;
  --primary-color-light: rgba(78, 111, 255, 0.1);
  --hover-bg: rgba(0, 0, 0, 0.04);
}

.dark {
  --sider-bg: #1a1a1a;
  --divider-color: #333333;
  --primary-color: #6d8cff;
  --primary-color-light: rgba(109, 140, 255, 0.15);
  --hover-bg: rgba(255, 255, 255, 0.06);
}

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.3);
}

.dark ::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.2);
}

.dark ::-webkit-scrollbar-thumb:hover {
  background-color: rgba(255, 255, 255, 0.3);
}
</style>
