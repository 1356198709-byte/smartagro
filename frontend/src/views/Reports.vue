<template>
  <div>
    <div class="page-header">
      <h2>{{ $t('reports.title') }}</h2>
      <div style="display:flex; gap:10px;">
        <button class="btn btn-primary" @click="showWorkReport = true">+ {{ $t('reports.work_reports') }}</button>
      </div>
    </div>

    <!-- Profitability -->
    <div class="card">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h3>{{ $t('reports.profitability') }}</h3>
        <button class="btn btn-primary" @click="exportExcel" style="height:36px;">
          📥 {{ $t('reports.export') }} Excel
        </button>
      </div>
      <table>
        <thead>
          <tr>
            <th>{{ $t('dashboard.field') }}</th>
            <th>{{ $t('lands.area') }}</th>
            <th>{{ $t('reports.total_cost') }}</th>
            <th>{{ $t('dashboard.cost_per_ha') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in store.profitability" :key="p.plot_id">
            <td>{{ p.plot_name }}</td>
            <td>{{ p.area_ha }} ha</td>
            <td>¥{{ p.total_material_cost }}</td>
            <td>¥{{ p.cost_per_ha }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Work Reports -->
    <div class="card">
      <h3>{{ $t('reports.work_reports') }}</h3>
      <div style="margin-bottom:12px;">
        <label>{{ $t('tasks.assigned') }} ID: </label>
        <input v-model.number="reportTaskId" type="number" style="padding:6px; border-radius:6px; border:1px solid #ddd; width:100px;" />
        <button class="btn btn-primary" @click="fetchReports" style="margin-left:8px;">{{ $t('common.search') }}</button>
      </div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>{{ $t('tasks.assigned') }}</th>
            <th>{{ $t('reports.progress') }}</th>
            <th>{{ $t('reports.report_text') }}</th>
            <th>{{ $t('reports.geo') }}</th>
            <th>{{ $t('tasks.planned_start') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in store.workReports" :key="r.id">
            <td>{{ r.id }}</td>
            <td>{{ r.task_id }}</td>
            <td>
              <div style="background:#eee; border-radius:10px; height:20px; width:100%;">
                <div :style="{ width: r.progress_percent + '%', background: '#2d6a4f', height: '100%', borderRadius: '10px', minWidth: '2px' }"></div>
              </div>
              {{ r.progress_percent }}%
            </td>
            <td>{{ r.report_text }}</td>
            <td>{{ r.geo_latitude?.toFixed(4) }}, {{ r.geo_longitude?.toFixed(4) }}</td>
            <td>{{ r.reported_at?.split('T')[0] }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Work Report Modal -->
    <div v-if="showWorkReport" class="modal-overlay" @click.self="showWorkReport = false">
      <div class="modal">
        <h3>{{ $t('reports.work_reports') }}</h3>
        <div class="form-group">
          <label>{{ $t('tasks.assigned') }} ID</label>
          <input v-model.number="wrForm.task_id" type="number" required />
        </div>
        <div class="form-group">
          <label>{{ $t('reports.progress') }} (%)</label>
          <input v-model.number="wrForm.progress_percent" type="number" min="0" max="100" required />
        </div>
        <div class="form-group">
          <label>{{ $t('reports.report_text') }}</label>
          <textarea v-model="wrForm.report_text" rows="3"></textarea>
        </div>
        <div class="form-group">
          <label>{{ $t('reports.geo') }} (lat)</label>
          <input v-model.number="wrForm.geo_latitude" type="number" step="0.0001" />
        </div>
        <div class="form-group">
          <label>{{ $t('reports.geo') }} (lng)</label>
          <input v-model.number="wrForm.geo_longitude" type="number" step="0.0001" />
        </div>
        <div class="modal-actions">
          <button class="btn" @click="showWorkReport = false">{{ $t('common.cancel') }}</button>
          <button class="btn btn-primary" @click="doSubmitReport">{{ $t('common.save') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useDataStore } from '../stores/data'
import { api } from '../stores/data'

const store = useDataStore()
const showWorkReport = ref(false)
const reportTaskId = ref(1)

const wrForm = ref({
  task_id: 1, progress_percent: 0, report_text: '', geo_latitude: null, geo_longitude: null,
})

onMounted(async () => {
  await Promise.all([
    store.fetchProfitability(),
    store.fetchWorkReports(1),
  ])
})

async function fetchReports() {
  await store.fetchWorkReports(reportTaskId.value)
}

async function doSubmitReport() {
  await store.createWorkReport(wrForm.value)
  showWorkReport.value = false
  wrForm.value = { task_id: 1, progress_percent: 0, report_text: '', geo_latitude: null, geo_longitude: null }
}

async function exportExcel() {
  try {
    const lang = localStorage.getItem('lang') || 'zh'
    const response = await api.get('/reports/profitability/excel', {
      params: { lang },
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', lang === 'ru' ? 'rentabelnost.xlsx' : 'profitability.xlsx')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (e) {
    console.error('Export failed:', e)
    alert('导出失败 / Ошибка экспорта')
  }
}
</script>

<style scoped>
h3 {
  font-size: 16px;
  margin-bottom: 12px;
}
</style>
