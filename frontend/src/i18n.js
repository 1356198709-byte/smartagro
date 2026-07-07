import { createI18n } from 'vue-i18n'
import ru from './locales/ru.json'
import zh from './locales/zh.json'

const savedLang = localStorage.getItem('lang') || 'zh'

const i18n = createI18n({
  legacy: false,
  locale: savedLang,
  fallbackLocale: 'zh',
  messages: { ru, zh },
})

export default i18n
