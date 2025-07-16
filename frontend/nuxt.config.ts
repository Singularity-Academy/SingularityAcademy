// https://nuxt.com/docs/api/configuration/nuxt-config
import AutoImport from 'unplugin-auto-import/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'
import { resolve } from 'path'

export default defineNuxtConfig({
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },

  modules: [
    '@nuxt/content',
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/test-utils',
    '@pinia/nuxt',
    'pinia-plugin-persistedstate/nuxt',
    '@nuxtjs/tailwindcss',
    'nuxtjs-naive-ui',
    'nuxt-lucide-icons',
    '@nuxtjs/i18n'
  ],

  lucide: {
    namePrefix: 'Icon'
  },

  vite: {
    plugins: [
      AutoImport({
        imports: [
          {
            'naive-ui': [
              'useDialog',
              'useMessage',
              'useNotification',
              'useLoadingBar'
            ]
          }
        ]
      }),
      Components({
        resolvers: [NaiveUiResolver()]
      })
    ]
  },

  nitro: {
    esbuild: {
      options: {
        target: 'esnext',
      },
    },
  },

  build: {
    transpile: ['naive-ui', 'vueuc'],
  },

  i18n: {
    locales: [
      { code: 'en', name: 'English', file: 'en/translation.json' },
      { code: 'zh', name: '简体中文', file: 'zh/translation.json' },
      { code: 'es', name: 'Español', file: 'es/translation.json' },
      { code: 'fr', name: 'Français', file: 'fr/translation.json' },
      { code: 'de', name: 'Deutsch', file: 'de/translation.json' },
      { code: 'ja', name: '日本語', file: 'ja/translation.json' },
      { code: 'ar', name: 'العربية', file: 'ar/translation.json' }
    ],
    lazy: true,
    skipSettingLocaleOnNavigate: true,
    langDir: resolve(__dirname, 'app/locales'),
    defaultLocale: 'zh',
    strategy: 'no_prefix'
  }
})