import { useThemeStore } from '~/stores/theme'

export default defineNuxtPlugin(() => {
    const themeStore = useThemeStore()

    watchEffect(() => {
        const html = document.documentElement
        html.classList.remove('dark', 'light')
        html.classList.add(themeStore.actualTheme)
    })
})