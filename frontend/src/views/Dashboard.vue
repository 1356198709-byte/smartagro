<template>
  <div>
    <div class="page-header">
      <h2>{{ $t('dashboard.title') }}</h2>
      <div style="display:flex; align-items:center; gap:12px;">
        <span v-if="lastRefresh" style="font-size:12px; color:#999;">🕐 {{ lastRefresh }}</span>
        <button class="btn" @click="refreshAll" style="height:30px; font-size:12px;">🔄 {{ $t('common.refresh') }}</button>
      </div>
    </div>

    <div class="stats-grid" v-if="store.analytics">
      <div class="stat-card">
        <div class="stat-value">{{ store.analytics.total_land_area }}</div>
        <div class="stat-label">{{ $t('dashboard.total_area') }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ store.analytics.total_plots }}</div>
        <div class="stat-label">{{ $t('dashboard.total_plots') }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ store.analytics.active_tasks }}</div>
        <div class="stat-label">{{ $t('dashboard.active_tasks') }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ store.analytics.completed_tasks }}</div>
        <div class="stat-label">{{ $t('dashboard.completed_tasks') }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">¥{{ store.analytics.total_resources_value }}</div>
        <div class="stat-label">{{ $t('dashboard.resources_value') }}</div>
      </div>
      <div class="stat-card" :class="{ 'stat-danger': store.analytics.low_stock_resources > 0 }">
        <div class="stat-value">{{ store.analytics.low_stock_resources }}</div>
        <div class="stat-label">{{ $t('dashboard.low_stock') }}</div>
      </div>
    </div>

    <div style="display:flex; gap: 20px; flex-wrap: wrap;">
      <div class="card" style="flex:1; min-width:350px;">
        <h3>{{ $t('dashboard.recent_tasks') }}</h3>
        <table>
          <thead>
            <tr>
              <th>{{ $t('tasks.title') }}</th>
              <th>{{ $t('tasks.status') }}</th>
              <th>{{ $t('tasks.type') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in store.tasks.slice(0, 5)" :key="t.id">
              <td>{{ t.title }}</td>
              <td><span :class="statusBadge(t.status)">{{ $t('tasks.statuses.' + t.status) }}</span></td>
              <td>{{ $t('tasks.types.' + t.task_type) }}</td>
            </tr>
            <tr v-if="store.tasks.length === 0">
              <td colspan="3" style="text-align:center;color:#999;">{{ $t('common.no_data') }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="card" style="flex:1; min-width:350px;">
        <h3>{{ $t('dashboard.profitability') }}</h3>
        <table>
          <thead>
            <tr>
              <th>{{ $t('dashboard.field') }}</th>
              <th>{{ $t('reports.total_cost') }}</th>
              <th>{{ $t('dashboard.cost_per_ha') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in store.profitability" :key="p.plot_id">
              <td>{{ p.plot_name }}</td>
              <td>¥{{ p.total_material_cost }}</td>
              <td>¥{{ p.cost_per_ha }}</td>
            </tr>
            <tr v-if="store.profitability.length === 0">
              <td colspan="3" style="text-align:center;color:#999;">{{ $t('common.no_data') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useDataStore } from '../stores/data'

const store = useDataStore()
const lastRefresh = ref('')
const autoRefresh = ref(true)
let timer = null

async function refreshAll() {
  await Promise.all([
    store.fetchLands(),
    store.fetchTasks(),
    store.fetchResources(),
    store.fetchAnalytics(),
    store.fetchProfitability(),
  ])
  lastRefresh.value = new Date().toLocaleTimeString()
}

onMounted(async () => {
  await refreshAll()
  // 每30秒自动刷新
  timer = setInterval(refreshAll, 30000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

function statusBadge(status) {
  const map = {
    pending: 'badge badge-warning',
    in_progress: 'badge badge-info',
    completed: 'badge badge-success',
    cancelled: 'badge badge-danger',
  }
  return map[status] || ''
}
</script>

<style scoped>
.stats-grid {
  display: flex;
  gap: 14px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.stat-danger {
  border: 2px solid var(--danger);
}

.stat-danger .stat-value {
  color: var(--danger);
}

h3 {
  font-size: 16px;
  margin-bottom: 12px;
}
</style>
