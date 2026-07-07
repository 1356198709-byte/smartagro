<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <h1>{{ $t('app.title') }}</h1>
        <p>{{ $t('app.subtitle') }}</p>
      </div>

      <div v-if="isRegister" class="login-form">
        <h2>{{ $t('auth.register') }}</h2>
        <div class="form-group">
          <label>{{ $t('auth.username') }}</label>
          <input v-model="form.username" type="text" required />
        </div>
        <div class="form-group">
          <label>{{ $t('auth.email') }}</label>
          <input v-model="form.email" type="email" required />
        </div>
        <div class="form-group">
          <label>{{ $t('auth.password') }}</label>
          <input v-model="form.password" type="password" required />
        </div>
        <div class="form-group">
          <label>{{ $t('auth.full_name') }}</label>
          <input v-model="form.full_name" type="text" />
        </div>
        <div class="form-group">
          <label>{{ $t('auth.role') }}</label>
          <select v-model="form.role">
            <option value="admin">{{ $t('auth.roles.admin') }}</option>
            <option value="dispatcher">{{ $t('auth.roles.dispatcher') }}</option>
            <option value="field_staff">{{ $t('auth.roles.field_staff') }}</option>
            <option value="storekeeper">{{ $t('auth.roles.storekeeper') }}</option>
          </select>
        </div>
        <button class="btn btn-primary" @click="doRegister" style="width:100%">
          {{ $t('auth.submit_register') }}
        </button>
        <p class="switch-link">
          {{ $t('auth.has_account') }}
          <a href="#" @click.prevent="isRegister = false">{{ $t('auth.submit_login') }}</a>
        </p>
      </div>

      <div v-else class="login-form">
        <h2>{{ $t('auth.login') }}</h2>
        <div class="form-group">
          <label>{{ $t('auth.username') }}</label>
          <input v-model="loginForm.username" type="text" required />
        </div>
        <div class="form-group">
          <label>{{ $t('auth.password') }}</label>
          <input v-model="loginForm.password" type="password" required @keyup.enter="doLogin" />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button class="btn btn-primary" @click="doLogin" style="width:100%">
          {{ $t('auth.submit_login') }}
        </button>
        <p class="switch-link">
          {{ $t('auth.no_account') }}
          <a href="#" @click.prevent="isRegister = true">{{ $t('auth.submit_register') }}</a>
        </p>
      </div>

      <div class="lang-toggle">
        <button class="btn btn-primary" @click="toggleLang">
          {{ $t('app.lang_switch') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../stores/auth'
import i18n from '../i18n'

const router = useRouter()
const { locale } = useI18n()
const auth = useAuthStore()

const isRegister = ref(false)
const error = ref('')

const loginForm = ref({ username: '', password: '' })
const form = ref({
  username: '',
  email: '',
  password: '',
  full_name: '',
  role: 'field_staff',
})

function toggleLang() {
  const newLang = i18n.global.locale.value === 'ru' ? 'zh' : 'ru'
  i18n.global.locale.value = newLang
  locale.value = newLang
  localStorage.setItem('lang', newLang)
}

async function doLogin() {
  error.value = ''
  try {
    await auth.login(loginForm.value.username, loginForm.value.password)
    router.push('/')
  } catch (e) {
    error.value = e.response?.data?.detail || i18n.global.t('common.login_failed')
  }
}

async function doRegister() {
  error.value = ''
  try {
    await auth.register(form.value)
    isRegister.value = false
    loginForm.value.username = form.value.username
    loginForm.value.password = form.value.password
    error.value = i18n.global.t('common.register_success')
  } catch (e) {
    error.value = e.response?.data?.detail || i18n.global.t('common.register_failed')
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 50%, #40916c 100%);
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  width: 90%;
  max-width: 420px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 24px;
}

.login-header h1 {
  font-size: 28px;
  color: var(--primary-dark);
}

.login-header p {
  font-size: 12px;
  color: var(--gray-600);
  margin-top: 4px;
}

.login-form h2 {
  font-size: 18px;
  margin-bottom: 16px;
  text-align: center;
}

.switch-link {
  text-align: center;
  margin-top: 14px;
  font-size: 13px;
  color: var(--gray-600);
}

.switch-link a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 600;
}

.error-msg {
  color: var(--danger);
  font-size: 13px;
  margin-bottom: 8px;
  text-align: center;
}

.lang-toggle {
  margin-top: 16px;
  text-align: center;
}

.lang-toggle .btn {
  background: var(--gray-100) !important;
  color: var(--gray-800) !important;
  border: 1px solid var(--gray-300) !important;
}
</style>
