import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import i18n from './i18n'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)

app.config.errorHandler = (err, vm, info) => {
  document.body.innerHTML = '<div style="padding:40px;color:red;font-size:18px;"><h2>Vue Error</h2><pre>' + err + '</pre><p>' + info + '</p></div>'
}

window.onerror = (msg, url, line, col, err) => {
  document.body.innerHTML = '<div style="padding:40px;color:red;font-size:18px;"><h2>JS Error</h2><pre>' + (err?.message || msg) + '</pre><p>Line: ' + line + '</p></div>'
}

app.mount('#app')
