<script setup lang="ts">
import {RouterLink} from "vue-router";
import {type MenuOption, NIcon} from "naive-ui";
import {IconHouse, IconLayoutDashboard} from "#components";

const emit = defineEmits<{
  (e: 'navigate'): void
}>()

const route = useRoute()

const activeKey = ref<string>('')

function getActiveKey(path: string): string {
  if (path === '/') return 'go-back-home'
  if (path.startsWith('/dashboard')) return 'go-to-dashboard'
  return ''
}

activeKey.value = getActiveKey(route.path)

watch(() => route.path, (newPath) => {
  activeKey.value = getActiveKey(newPath)
})

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

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
</script>

<template>
  <div class="flex py-3 px-7 justify-between w-full items-center">
    <n-text>Calrif AI 知澜</n-text>

    <div class="">
      <n-menu
          mode="horizontal"
          :options="menuOptions"
          v-model:value="activeKey"
      />
    </div>

  </div>
</template>

<style scoped lang="scss">

</style>