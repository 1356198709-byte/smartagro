<template>
  <div>
    <div class="page-header">
      <h2>{{ $t('lands.title') }}</h2>
      <div style="display:flex; gap:10px;">
        <button class="btn btn-primary" @click="toggleMapView">
          🗺️ {{ showMap ? $t('common.close') : $t('lands.map_view') }}
        </button>
        <button class="btn btn-primary" @click="openAdd">{{ $t('lands.add') }}</button>
        <button class="btn" :class="showHelp ? 'btn-warning' : 'btn-primary'" @click="showHelp = !showHelp">
          ❓ {{ $t('lands.howto_title') }}
        </button>
      </div>
    </div>

    <!-- Help -->
    <div v-if="showHelp" class="card help-box">
      <ol>
        <li v-html="$t('lands.howto_step1')"></li>
        <li v-html="$t('lands.howto_step2')"></li>
        <li v-html="$t('lands.howto_step3')"></li>
        <li v-html="$t('lands.howto_step4')"></li>
        <li v-html="$t('lands.howto_step5')"></li>
      </ol>
    </div>

    <!-- Map View -->
    <div v-if="showMap" class="card" style="height:400px; padding:0; overflow:hidden;">
      <div ref="mapContainer" style="width:100%; height:100%;"></div>
    </div>

    <!-- Table -->
    <div class="card">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>{{ $t('lands.name') }}</th>
            <th>{{ $t('lands.cadastral') }}</th>
            <th>{{ $t('lands.area') }}</th>
            <th>{{ $t('lands.soil') }}</th>
            <th>{{ $t('lands.status') }}</th>
            <th>{{ $t('common.actions') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="plot in store.lands" :key="plot.id">
            <td>{{ plot.id }}</td>
            <td>{{ plot.name }}</td>
            <td>{{ plot.cadastral_number }}</td>
            <td>{{ plot.area_ha }}</td>
            <td>{{ plot.soil_type }}</td>
            <td>{{ plot.status }}</td>
            <td>
              <div style="display:flex; gap:6px;">
                <button class="btn btn-primary" @click="locatePlot(plot)" :title="$t('lands.locate_tooltip')">📍</button>
                <button class="btn btn-primary" @click="openRotations(plot)">🔄</button>
                <button class="btn btn-warning" @click="openEdit(plot)">✏️</button>
                <button class="btn btn-danger" @click="doDelete(plot.id)">🗑️</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <h3>{{ editing ? $t('lands.edit') : $t('lands.add') }}</h3>
        <div class="form-group">
          <label>{{ $t('lands.name') }}</label>
          <input v-model="form.name" type="text" required />
        </div>
        <div class="form-group">
          <label>{{ $t('lands.cadastral') }}</label>
          <input v-model="form.cadastral_number" type="text" required />
        </div>
        <div class="form-group">
          <label>{{ $t('lands.area') }}</label>
          <input v-model.number="form.area_ha" type="number" step="0.01" required />
        </div>
        <div class="form-group">
          <label>{{ $t('lands.soil') }}</label>
          <input v-model="form.soil_type" type="text" />
        </div>
        <div class="form-group">
          <label>{{ $t('lands.geometry') }}</label>
          <div style="display:flex; gap:8px; margin-bottom:8px;">
            <input v-model="geoLat" type="number" step="0.0001" :placeholder="$t('lands.lat_placeholder')" style="flex:1;" />
            <input v-model="geoLng" type="number" step="0.0001" :placeholder="$t('lands.lng_placeholder')" style="flex:1;" />
            <button class="btn btn-primary" type="button" @click="genPoint">📍 点</button>
            <button class="btn btn-primary" type="button" @click="genSquare">⬜ 矩形</button>
          </div>
          <textarea v-model="form.geometry" rows="2" :placeholder="$t('lands.geo_placeholder')"></textarea>
          <small style="color:#888;">{{ $t('lands.geo_hint') }}</small>
        </div>
        <div class="modal-actions">
          <button class="btn" @click="showModal = false">{{ $t('common.cancel') }}</button>
          <button class="btn btn-primary" @click="doSave">{{ $t('common.save') }}</button>
        </div>
      </div>
    </div>

    <!-- Rotations Modal -->
    <div v-if="showRotations" class="modal-overlay" @click.self="showRotations = false">
      <div class="modal">
        <h3>{{ $t('lands.rotations') }} - {{ selectedPlot?.name }}</h3>
        <table>
          <thead>
            <tr>
              <th>{{ $t('lands.crop_name') }}</th>
              <th>{{ $t('lands.sowing_date') }}</th>
              <th>{{ $t('lands.harvest_date') }}</th>
              <th>{{ $t('lands.yield') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in (store.rotations[selectedPlot?.id] || [])" :key="r.id">
              <td>{{ r.crop_name }}</td>
              <td>{{ r.sowing_date?.split('T')[0] }}</td>
              <td>{{ r.harvest_date?.split('T')[0] }}</td>
              <td>{{ r.yield_amount }}</td>
            </tr>
          </tbody>
        </table>
        <div style="margin-top:16px;border-top:1px solid #eee;padding-top:16px;">
          <div class="form-group">
            <label>{{ $t('lands.crop_name') }}</label>
            <input v-model="rotForm.crop_name" type="text" />
          </div>
          <div class="form-group">
            <label>{{ $t('lands.sowing_date') }}</label>
            <input v-model="rotForm.sowing_date" type="date" />
          </div>
          <div class="form-group">
            <label>{{ $t('lands.harvest_date') }}</label>
            <input v-model="rotForm.harvest_date" type="date" />
          </div>
          <div class="form-group">
            <label>{{ $t('lands.yield') }}</label>
            <input v-model.number="rotForm.yield_amount" type="number" step="0.1" />
          </div>
          <button class="btn btn-primary" @click="doAddRotation">{{ $t('common.save') }}</button>
        </div>
        <div class="modal-actions">
          <button class="btn" @click="showRotations = false">{{ $t('common.close') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useDataStore } from '../stores/data'
import i18n from '../i18n'

const store = useDataStore()
const showModal = ref(false)
const showRotations = ref(false)
const showMap = ref(false)
const showHelp = ref(false)
const editing = ref(null)
const selectedPlot = ref(null)
const mapContainer = ref(null)
let mapInstance = null
let plotLayers = {}
let highlightedLayer = null

const form = ref({
  name: '', cadastral_number: '', area_ha: 0, soil_type: '', geometry: '',
})
const geoLat = ref('')
const geoLng = ref('')

function genPoint() {
  const lat = parseFloat(geoLat.value)
  const lng = parseFloat(geoLng.value)
  if (isNaN(lat) || isNaN(lng)) return
  form.value.geometry = JSON.stringify({ type: 'Point', coordinates: [lng, lat] })
}

function genSquare() {
  const lat = parseFloat(geoLat.value)
  const lng = parseFloat(geoLng.value)
  if (isNaN(lat) || isNaN(lng)) return
  const d = 0.02
  form.value.geometry = JSON.stringify({
    type: 'Polygon',
    coordinates: [[
      [lng - d, lat - d],
      [lng + d, lat - d],
      [lng + d, lat + d],
      [lng - d, lat + d],
      [lng - d, lat - d],
    ]],
  })
}

const rotForm = ref({
  crop_name: '', sowing_date: '', harvest_date: '', yield_amount: 0, land_plot_id: 0,
})

onMounted(async () => {
  await store.fetchLands()
})

watch(showMap, async (val) => {
  if (val) {
    await nextTick()
    initMap()
  }
})

async function initMap() {
  const L = await import('leaflet')
  if (mapInstance) {
    mapInstance.remove()
  }
  mapInstance = L.map(mapContainer.value, { attributionControl: false }).setView([43.92, 81.29], 12)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(mapInstance)

  plotLayers = {}
  store.lands.forEach((plot) => {
    if (plot.geometry) {
      try {
        const geo = JSON.parse(plot.geometry)
        if (geo.type === 'Polygon') {
          const coords = geo.coordinates[0].map(([lng, lat]) => [lat, lng])
          const layer = L.polygon(coords, { color: '#22c55e', fillColor: '#22c55e', fillOpacity: 0.4, weight: 2 })
            .bindPopup(`<b>${plot.name}</b><br>${plot.area_ha} ha`)
            .addTo(mapInstance)
          plotLayers[plot.id] = layer
        } else if (geo.type === 'Point') {
          const [lng, lat] = geo.coordinates
          const layer = L.marker([lat, lng])
            .bindPopup(`<b>${plot.name}</b><br>${plot.area_ha} ha`)
            .addTo(mapInstance)
          plotLayers[plot.id] = layer
        }
      } catch (e) {
        // skip invalid geometries
      }
    }
  })
}

function toggleMapView() {
  showMap.value = !showMap.value
}

async function locatePlot(plot) {
  if (!showMap.value) {
    showMap.value = true
    await nextTick()
    initMap()
  }
  await nextTick()
  highlightPlot(plot)
}

function highlightPlot(plot) {
  if (!mapInstance || !plot.geometry) return
  if (highlightedLayer) {
    if (highlightedLayer.setStyle) {
      highlightedLayer.setStyle({ color: '#22c55e', fillColor: '#22c55e', fillOpacity: 0.4, weight: 2 })
    }
  }
  const layer = plotLayers[plot.id]
  if (!layer) return
  if (layer.setStyle) {
    layer.setStyle({ color: '#f97316', fillColor: '#f97316', fillOpacity: 0.6, weight: 4 })
  }
  highlightedLayer = layer
  try {
    const geo = JSON.parse(plot.geometry)
    if (geo.type === 'Polygon') {
      const coords = geo.coordinates[0].map(([lng, lat]) => [lat, lng])
      mapInstance.fitBounds(coords, { padding: [50, 50], maxZoom: 15 })
    } else if (geo.type === 'Point') {
      const [lng, lat] = geo.coordinates
      mapInstance.flyTo([lat, lng], 15)
    }
  } catch (e) {
    // skip
  }
  setTimeout(() => {
    if (layer.openPopup) layer.openPopup()
  }, 600)
}

function openAdd() {
  editing.value = null
  form.value = { name: '', cadastral_number: '', area_ha: 0, soil_type: '', geometry: '' }
  geoLat.value = ''
  geoLng.value = ''
  showModal.value = true
}

function openEdit(plot) {
  editing.value = plot.id
  form.value = {
    name: plot.name,
    cadastral_number: plot.cadastral_number,
    area_ha: plot.area_ha,
    soil_type: plot.soil_type,
    geometry: plot.geometry || '',
  }
  geoLat.value = ''
  geoLng.value = ''
  if (plot.geometry) {
    try {
      const geo = JSON.parse(plot.geometry)
      if (geo.type === 'Point') {
        geoLng.value = geo.coordinates[0]
        geoLat.value = geo.coordinates[1]
      } else if (geo.type === 'Polygon' && geo.coordinates[0].length >= 2) {
        const c = geo.coordinates[0][0]
        geoLng.value = c[0]
        geoLat.value = c[1]
      }
    } catch (e) { /* skip */ }
  }
  showModal.value = true
}

async function doSave() {
  if (editing.value) {
    await store.updateLand(editing.value, form.value)
  } else {
    await store.createLand(form.value)
  }
  showModal.value = false
}

async function doDelete(id) {
  if (!confirm(i18n.global.t('common.confirm_delete'))) return
  await store.deleteLand(id)
}

function openRotations(plot) {
  selectedPlot.value = plot
  rotForm.value.land_plot_id = plot.id
  store.fetchRotations(plot.id)
  showRotations.value = true
}

async function doAddRotation() {
  await store.createRotation(rotForm.value)
  rotForm.value = { crop_name: '', sowing_date: '', harvest_date: '', yield_amount: 0, land_plot_id: selectedPlot.value.id }
}
</script>

<style scoped>
.help-box {
  background: #eff6ff;
  border: 1px solid #93c5fd;
  border-radius: 8px;
  padding: 16px 24px;
}

.help-box ol {
  margin: 0;
  padding-left: 20px;
}

.help-box li {
  margin-bottom: 6px;
  line-height: 1.6;
  font-size: 14px;
}
</style>
