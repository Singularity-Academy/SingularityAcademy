import { createI18n } from 'vue-i18n'
import enTranslation from '~/locales/en/translation.json'
import esTranslation from '~/locales/es/translation.json'
import frTranslation from '~/locales/fr/translation.json'
import deTranslation from '~/locales/de/translation.json'
import jaTranslation from '~/locales/ja/translation.json'
import arTranslation from '~/locales/ar/translation.json'
import zhTranslation from '~/locales/zh/translation.json'

const messages = {
  en: enTranslation,
  es: esTranslation,
  fr: frTranslation,
  de: deTranslation,
  ja: jaTranslation,
  ar: arTranslation,
  zh: zhTranslation
}

export default defineNuxtPlugin((nuxtApp) => {
  const i18n = createI18n({
    legacy: false,
    locale: 'zh',
    fallbackLocale: 'en',
    messages
  })

  nuxtApp.vueApp.use(i18n)
})
