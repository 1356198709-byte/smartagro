<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>{{ $t('app.title') }}</h1>
        <p class="sidebar-subtitle">{{ $t('app.subtitle') }}</p>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item">
          <span>📊</span> {{ $t('nav.dashboard') }}
        </router-link>
        <router-link to="/lands" class="nav-item">
          <span>🗺️</span> {{ $t('nav.lands') }}
        </router-link>
        <router-link to="/tasks" class="nav-item">
          <span>📋</span> {{ $t('nav.tasks') }}
        </router-link>
        <router-link to="/resources" class="nav-item">
          <span>📦</span> {{ $t('nav.resources') }}
        </router-link>
        <router-link to="/reports" class="nav-item">
          <span>📈</span> {{ $t('nav.reports') }}
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info" v-if="auth.user">
          <strong>{{ auth.user.full_name || auth.user.username }}</strong>
          <small>{{ $t('auth.roles.' + auth.user.role) }}</small>
        </div>
        <button class="btn btn-primary lang-btn" @click="toggleLang">
          {{ $t('app.lang_switch') }}
        </button>
        <button class="btn btn-danger" @click="doLogout" style="width:100%">
          🚪 {{ $t('nav.logout') }}
        </button>
      </div>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../stores/auth'
import { useDataStore } from '../stores/data'
import i18n from '../i18n'

const router = useRouter()
const { locale } = useI18n()
const auth = useAuthStore()
const data = useDataStore()

async function toggleLang() {
  const newLang = i18n.global.locale.value === 'ru' ? 'zh' : 'ru'
  i18n.global.locale.value = newLang
  locale.value = newLang
  localStorage.setItem('lang', newLang)
  // 刷新数据（带新语言参数）
  await Promise.all([
    data.fetchLands(),
    data.fetchTasks(),
    data.fetchResources(),
    data.fetchAnalytics(),
    data.fetchProfitability(),
  ])
}

function doLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 240px;
  background: linear-gradient(180deg, #1b4332 0%, #2d6a4f 100%);
  color: white;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255,255,255,0.15);
}

.sidebar-header h1 {
  font-size: 20px;
  font-weight: 700;
}

.sidebar-subtitle {
  font-size: 11px;
  opacity: 0.75;
  margin-top: 4px;
}

.sidebar-nav {
  flex: 1;
  padding: 12px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.2s;
}

.nav-item:hover,
.nav-item.router-link-active {
  background: rgba(255,255,255,0.12);
  color: white;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255,255,255,0.15);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.user-info {
  text-align: center;
  margin-bottom: 4px;
}

.user-info strong {
  display: block;
  font-size: 14px;
}

.user-info small {
  font-size: 11px;
  opacity: 0.7;
}

.lang-btn {
  background: rgba(255,255,255,0.15) !important;
  border: 1px solid rgba(255,255,255,0.25) !important;
  width: 100%;
  justify-content: center;
}

.lang-btn:hover {
  background: rgba(255,255,255,0.25) !important;
}

.main-content {
  flex: 1;
  margin-left: 240px;
  padding: 24px;
}
</style>
