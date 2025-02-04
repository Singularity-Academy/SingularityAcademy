import i18next from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector'; // 语言检测插件
import enTranslation from './locales/en/translation.json';
import esTranslation from './locales/es/translation.json';
import frTranslation from './locales/fr/translation.json';
import deTranslation from './locales/de/translation.json';
import jaTranslation from './locales/ja/translation.json';
import arTranslation from './locales/ar/translation.json';
import zhTranslation from './locales/zh/translation.json';

const i18n = i18next
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        fallbackLng: 'en', // 默认语言
        debug: true, // 开启调试模式
        interpolation: { escapeValue: false },
        resources: {
            en: {
                translation: enTranslation,
            },
            es: {
                translation: esTranslation,
            },
            fr: {
                translation: frTranslation,
            },
            de: {
                translation: deTranslation,
            },
            ja: {
                translation: jaTranslation,
            },
            ar: {
                translation: arTranslation,
            },
            zh: {
                translation: zhTranslation,
            },
            zh_CN: {
                translation: zhTranslation,
            },
        },
        react: {
            useSuspense: false, // 确保不使用 Suspense
        },
        supportedLngs: ['en', 'es', 'fr', 'de', 'ja', 'ar', 'zh', 'zh_CN']
    });
export { i18next };
export default i18n
