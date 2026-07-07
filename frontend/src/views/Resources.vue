<template>
  <div>
    <div class="page-header">
      <h2>{{ $t('resources.title') }}</h2>
      <div style="display:flex; gap:10px;">
        <button class="btn btn-warning" @click="showConsumption = true">{{ $t('resources.consumption') }}</button>
        <button class="btn btn-primary" @click="openAdd">{{ $t('resources.add') }}</button>
      </div>
    </div>

    <!-- Low stock alert -->
    <div v-if="lowStockItems.length > 0" class="card" style="border-left:4px solid var(--danger); background:#fff5f5;">
      <strong style="color:var(--danger);">⚠️ {{ $t('resources.low_stock_warning') }}</strong>
      <span v-for="r in lowStockItems" :key="r.id" style="margin-left:10px;">
        {{ r.name }} ({{ r.quantity }} {{ r.unit }})
      </span>
    </div>

    <div class="card">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>{{ $t('resources.name') }}</th>
            <th>{{ $t('resources.type') }}</th>
            <th>{{ $t('resources.quantity') }}</th>
            <th>{{ $t('resources.unit') }}</th>
            <th>{{ $t('resources.min_threshold') }}</th>
            <th>{{ $t('resources.price') }}</th>
            <th>{{ $t('resources.supplier') }}</th>
            <th>{{ $t('common.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in store.resources" :key="r.id" :class="{ 'low-row': r.quantity <= r.min_threshold }">
            <td>{{ r.id }}</td>
            <td>{{ r.name }}</td>
            <td>{{ $t('resources.types.' + r.resource_type) }}</td>
            <td :style="{ color: r.quantity <= r.min_threshold ? 'var(--danger)' : 'inherit', fontWeight: '600' }">
              {{ r.quantity }}
            </td>
            <td>{{ r.unit }}</td>
            <td>{{ r.min_threshold }}</td>
            <td>¥{{ r.price_per_unit }}</td>
            <td>{{ r.supplier }}</td>
            <td>
              <div style="display:flex; gap:6px;">
                <button class="btn btn-warning" @click="openEdit(r)">✏️</button>
                <button class="btn btn-danger" @click="doDelete(r.id)">🗑️</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <h3>{{ editing ? $t('resources.edit') : $t('resources.add') }}</h3>
        <div class="form-group">
          <label>{{ $t('resources.name') }}</label>
          <input v-model="form.name" type="text" required />
        </div>
        <div class="form-group">
          <label>{{ $t('resources.type') }}</label>
          <select v-model="form.resource_type">
            <option value="seeds">{{ $t('resources.types.seeds') }}</option>
            <option value="fertilizer">{{ $t('resources.types.fertilizer') }}</option>
            <option value="fuel">{{ $t('resources.types.fuel') }}</option>
            <option value="pesticide">{{ $t('resources.types.pesticide') }}</option>
            <option value="other">{{ $t('resources.types.other') }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>{{ $t('resources.quantity') }}</label>
          <input v-model.number="form.quantity" type="number" step="0.01" required />
        </div>
        <div class="form-group">
          <label>{{ $t('resources.unit') }}</label>
          <input v-model="form.unit" type="text" required />
        </div>
        <div class="form-group">
          <label>{{ $t('resources.min_threshold') }}</label>
          <input v-model.number="form.min_threshold" type="number" step="0.01" />
        </div>
        <div class="form-group">
          <label>{{ $t('resources.price') }}</label>
          <input v-model.number="form.price_per_unit" type="number" step="0.01" />
        </div>
        <div class="form-group">
          <label>{{ $t('resources.supplier') }}</label>
          <input v-model="form.supplier" type="text" />
        </div>
        <div class="modal-actions">
          <button class="btn" @click="showModal = false">{{ $t('common.cancel') }}</button>
          <button class="btn btn-primary" @click="doSave">{{ $t('common.save') }}</button>
        </div>
      </div>
    </div>

    <!-- Consumption Modal -->
    <div v-if="showConsumption" class="modal-overlay" @click.self="showConsumption = false">
      <div class="modal">
        <h3>{{ $t('resources.consumption') }}</h3>
        <div class="form-group">
          <label>{{ $t('tasks.assigned') }} ID</label>
          <input v-model.number="consForm.task_id" type="number" required />
        </div>
        <div class="form-group">
          <label>{{ $t('resources.name') }}</label>
          <select v-model.number="consForm.resource_id">
            <option v-for="r in store.resources" :key="r.id" :value="r.id">{{ r.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>{{ $t('tasks.land') }} ID</label>
          <input v-model.number="consForm.land_plot_id" type="number" required />
        </div>
        <div class="form-group">
          <label>{{ $t('resources.quantity') }}</label>
          <input v-model.number="consForm.quantity_used" type="number" step="0.01" required />
        </div>
        <div class="modal-actions">
          <button class="btn" @click="showConsumption = false">{{ $t('common.cancel') }}</button>
          <button class="btn btn-primary" @click="doAddConsumption">{{ $t('common.save') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDataStore } from '../stores/data'
import i18n from '../i18n'

const store = useDataStore()
const showModal = ref(false)
const showConsumption = ref(false)
const editing = ref(null)

const form = ref({
  name: '', resource_type: 'other', unit: '', quantity: 0, min_threshold: 0, price_per_unit: 0, supplier: '',
})

const consForm = ref({
  task_id: 1, resource_id: 1, land_plot_id: 1, quantity_used: 0,
})

const lowStockItems = computed(() =>
  store.resources.filter((r) => r.quantity <= r.min_threshold)
)

onMounted(async () => {
  await store.fetchResources()
})

function openAdd() {
  editing.value = null
  form.value = { name: '', resource_type: 'other', unit: '', quantity: 0, min_threshold: 0, price_per_unit: 0, supplier: '' }
  showModal.value = true
}

function openEdit(r) {
  editing.value = r.id
  form.value = { ...r }
  showModal.value = true
}

async function doSave() {
  if (editing.value) {
    await store.updateResource(editing.value, form.value)
  } else {
    await store.createResource(form.value)
  }
  showModal.value = false
}

async function doDelete(id) {
  if (!confirm(i18n.global.t('common.confirm_delete'))) return
  await store.deleteResource(id)
}

async function doAddConsumption() {
  try {
    await store.addConsumption(consForm.value)
    showConsumption.value = false
    consForm.value = { task_id: 1, resource_id: 1, land_plot_id: 1, quantity_used: 0 }
  } catch (e) {
    alert(e.response?.data?.detail || i18n.global.t('common.error'))
  }
}
</script>

<style scoped>
.low-row {
  background: #fff5f5 !important;
}
</style>
