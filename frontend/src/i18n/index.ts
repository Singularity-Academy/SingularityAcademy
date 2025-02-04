import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import enTranslation from '../locales/en/translation.json';
import esTranslation from '../locales/es/translation.json';
import frTranslation from '../locales/fr/translation.json';
import deTranslation from '../locales/de/translation.json';
import jaTranslation from '../locales/ja/translation.json';
import arTranslation from '../locales/ar/translation.json';
import zhTranslation from '../locales/zh/translation.json';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: enTranslation },
      es: { translation: esTranslation },
      fr: { translation: frTranslation },
      de: { translation: deTranslation },
      ja: { translation: jaTranslation },
      ar: { translation: arTranslation },
      zh: { translation: zhTranslation },
      zh_CN: { translation: zhTranslation }
    },
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    },
    supportedLngs: ['en', 'es', 'fr', 'de', 'ja', 'ar', 'zh', 'zh_CN']
  });

export default i18n; 