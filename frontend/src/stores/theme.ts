import { ref, onMounted, watch, computed } from 'vue'
import { defineStore } from 'pinia'

type ThemeMode = 'light' | 'dark' | 'auto'

export const useThemeStore = defineStore('theme', () => {

    const themeName = ref<ThemeMode>('auto')

    const prefersDark = ref(false)

    const setupSystemThemeListener = () => {
        if (import.meta.client && window.matchMedia) {
            const media = window.matchMedia('(prefers-color-scheme: dark)')
            prefersDark.value = media.matches
            media.addEventListener('change', (e) => {
                prefersDark.value = e.matches
            })
        }
    }

    const actualTheme = computed(() => {
        if (themeName.value === 'auto') {
            return prefersDark.value ? 'dark' : 'light'
        }
        return themeName.value
    })

    const initTheme = () => {
        if (import.meta.client) {
            const saved = localStorage.getItem('theme') as ThemeMode | null
            if (saved === 'light' || saved === 'dark' || saved === 'auto') {
                themeName.value = saved
            } else {
                themeName.value = 'auto'
            }
        }
    }

    const toggleTheme = () => {
        themeName.value =
            themeName.value === 'light'
                ? 'dark'
                : themeName.value === 'dark'
                    ? 'auto'
                    : 'light'
    }

    watch(themeName, (val) => {
        if (import.meta.client) {
            localStorage.setItem('theme', val)
        }
    })

    onMounted(() => {
        initTheme()
        setupSystemThemeListener()
    })

    return {
        themeName,
        actualTheme,
        toggleTheme,
        initTheme,
    }
}, {
    persist: true
})