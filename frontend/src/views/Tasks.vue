<template>
  <div>
    <div class="page-header">
      <h2>{{ $t('tasks.title') }}</h2>
      <button class="btn btn-primary" @click="openAdd">{{ $t('tasks.add') }}</button>
    </div>

    <div class="card">
      <div style="margin-bottom:12px; display:flex; gap:10px; align-items:center;">
        <label style="font-weight:600;">{{ $t('tasks.status') }}:</label>
        <select v-model="filterStatus" @change="fetchFiltered" style="padding:6px 10px; border-radius:6px; border:1px solid #ddd;">
          <option value="">{{ $t('common.search') }}...</option>
          <option value="pending">{{ $t('tasks.statuses.pending') }}</option>
          <option value="in_progress">{{ $t('tasks.statuses.in_progress') }}</option>
          <option value="completed">{{ $t('tasks.statuses.completed') }}</option>
          <option value="cancelled">{{ $t('tasks.statuses.cancelled') }}</option>
        </select>
      </div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>{{ $t('tasks.type') }}</th>
            <th>{{ $t('tasks.title_field') }}</th>
            <th>{{ $t('tasks.land') }}</th>
            <th>{{ $t('tasks.status') }}</th>
            <th>{{ $t('tasks.planned_start') }}</th>
            <th>{{ $t('tasks.priority') }}</th>
            <th>{{ $t('common.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in store.tasks" :key="t.id">
            <td>{{ t.id }}</td>
            <td>{{ $t('tasks.types.' + t.task_type) }}</td>
            <td>{{ t.title }}</td>
            <td>#{{ t.land_plot_id }}</td>
            <td><span :class="statusBadge(t.status)">{{ $t('tasks.statuses.' + t.status) }}</span></td>
            <td>{{ t.planned_start?.split('T')[0] }}</td>
            <td>{{ '⭐'.repeat(t.priority) }}</td>
            <td>
              <div style="display:flex; gap:6px;">
                <button class="btn btn-warning" @click="openEdit(t)">✏️</button>
                <button class="btn btn-danger" @click="doDelete(t.id)">🗑️</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <h3>{{ editing ? $t('tasks.edit') : $t('tasks.add') }}</h3>
        <div class="form-group">
          <label>{{ $t('tasks.description') }}</label>
          <input v-model="form.title" type="text" required />
        </div>
        <div class="form-group">
          <label>{{ $t('tasks.type') }}</label>
          <select v-model="form.task_type">
            <option value="plowing">{{ $t('tasks.types.plowing') }}</option>
            <option value="sowing">{{ $t('tasks.types.sowing') }}</option>
            <option value="harvesting">{{ $t('tasks.types.harvesting') }}</option>
            <option value="fertilizing">{{ $t('tasks.types.fertilizing') }}</option>
            <option value="irrigation">{{ $t('tasks.types.irrigation') }}</option>
            <option value="other">{{ $t('tasks.types.other') }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>{{ $t('tasks.land') }} ID</label>
          <select v-model.number="form.land_plot_id">
            <option v-for="p in store.lands" :key="p.id" :value="p.id">{{ p.name }} ({{ p.id }})</option>
          </select>
        </div>
        <div class="form-group">
          <label>{{ $t('tasks.assigned') }} ID</label>
          <input v-model.number="form.assigned_to" type="number" />
        </div>
        <div class="form-group">
          <label>{{ $t('tasks.planned_start') }}</label>
          <input v-model="form.planned_start" type="datetime-local" required />
        </div>
        <div class="form-group">
          <label>{{ $t('tasks.planned_end') }}</label>
          <input v-model="form.planned_end" type="datetime-local" required />
        </div>
        <div class="form-group">
          <label>{{ $t('tasks.priority') }}</label>
          <select v-model.number="form.priority">
            <option :value="1">⭐</option>
            <option :value="2">⭐⭐</option>
            <option :value="3">⭐⭐⭐</option>
          </select>
        </div>
        <div class="form-group" v-if="editing">
          <label>{{ $t('tasks.status') }}</label>
          <select v-model="form.status">
            <option value="pending">{{ $t('tasks.statuses.pending') }}</option>
            <option value="in_progress">{{ $t('tasks.statuses.in_progress') }}</option>
            <option value="completed">{{ $t('tasks.statuses.completed') }}</option>
            <option value="cancelled">{{ $t('tasks.statuses.cancelled') }}</option>
          </select>
        </div>
        <div class="modal-actions">
          <button class="btn" @click="showModal = false">{{ $t('common.cancel') }}</button>
          <button class="btn btn-primary" @click="doSave">{{ $t('common.save') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useDataStore, api } from '../stores/data'
import i18n from '../i18n'

const store = useDataStore()
const showModal = ref(false)
const editing = ref(null)
const filterStatus = ref('')

const form = ref({
  title: '', task_type: 'other', land_plot_id: 1, assigned_to: 2,
  planned_start: '', planned_end: '', priority: 1, status: 'pending',
})

onMounted(async () => {
  await Promise.all([store.fetchTasks(), store.fetchLands()])
})

async function fetchFiltered() {
  const params = {}
  if (filterStatus.value) params.status = filterStatus.value
  const { data } = await api.get('/tasks/', { params })
  store.tasks = data
}

function openAdd() {
  editing.value = null
  form.value = {
    title: '', task_type: 'other', land_plot_id: store.lands[0]?.id || 1,
    assigned_to: 2, planned_start: '', planned_end: '', priority: 1, status: 'pending',
  }
  showModal.value = true
}

function openEdit(t) {
  editing.value = t.id
  form.value = {
    title: t.title, task_type: t.task_type, land_plot_id: t.land_plot_id,
    assigned_to: t.assigned_to, planned_start: t.planned_start?.slice(0, 16),
    planned_end: t.planned_end?.slice(0, 16), priority: t.priority, status: t.status,
  }
  showModal.value = true
}

async function doSave() {
  if (editing.value) {
    await store.updateTask(editing.value, form.value)
  } else {
    await store.createTask(form.value)
  }
  showModal.value = false
}

async function doDelete(id) {
  if (!confirm(i18n.global.t('common.confirm_delete'))) return
  await store.deleteTask(id)
}

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
