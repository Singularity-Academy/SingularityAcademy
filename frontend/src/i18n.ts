import i18next from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import { content } from './content';

const i18n = i18next
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        fallbackLng: 'en',
        debug: false,
        interpolation: { escapeValue: false },
        resources: {
            en: {
                translation: content.en,
            },
            zh: {
                translation: content.zh,
            },
        },
        react: {
            useSuspense: false,
        },
        supportedLngs: ['en', 'zh']
    });
export { i18next };
export default i18n
