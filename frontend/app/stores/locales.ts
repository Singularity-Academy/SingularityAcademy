import { defineStore } from 'pinia'
const { locale } = useI18n()

export const useLocaleStore = defineStore('locale', {
    state: () => ({
        lang: 'zh'
    }),
    persist: true,
    actions: {
        changeLang(lang: string) {
            this.lang = lang
            const { $i18n } = useNuxtApp()
            $i18n.setLocale(lang as typeof locale.value)
        }
    }
})
