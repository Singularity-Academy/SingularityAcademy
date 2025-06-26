// https://nuxt.com/docs/api/configuration/nuxt-config
import AutoImport from 'unplugin-auto-import/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'

export default defineNuxtConfig({
  srcDir: "src/",
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
    'nuxt-lucide-icons'
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
  plugins: [
    '~/i18n/index.ts'
  ],
})