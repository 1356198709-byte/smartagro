import { defineStore } from 'pinia'
import axios from 'axios'

export const api = axios.create({
  baseURL: '/api',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  // 自动附带语言参数
  const lang = localStorage.getItem('lang') || 'zh'
  config.params = { ...config.params, lang }
  return config
})

export const useDataStore = defineStore('data', {
  state: () => ({
    lands: [],
    tasks: [],
    resources: [],
    rotations: {},
    consumptions: [],
    workReports: [],
    analytics: null,
    profitability: [],
  }),
  actions: {
    // Lands
    async fetchLands() {
      const { data } = await api.get('/lands/')
      this.lands = data
    },
    async createLand(form) {
      const { data } = await api.post('/lands/', form)
      await this.fetchLands()
      return data
    },
    async updateLand(id, form) {
      const { data } = await api.put(`/lands/${id}`, form)
      await this.fetchLands()
      return data
    },
    async deleteLand(id) {
      await api.delete(`/lands/${id}`)
      await this.fetchLands()
    },

    // Rotations
    async fetchRotations(plotId) {
      const { data } = await api.get(`/lands/${plotId}/rotations`)
      this.rotations[plotId] = data
    },
    async createRotation(form) {
      const { data } = await api.post('/lands/rotations', form)
      await this.fetchRotations(form.land_plot_id)
      return data
    },

    // Tasks
    async fetchTasks() {
      const { data } = await api.get('/tasks/')
      this.tasks = data
    },
    async createTask(form) {
      const { data } = await api.post('/tasks/', form)
      await this.fetchTasks()
      return data
    },
    async updateTask(id, form) {
      const { data } = await api.put(`/tasks/${id}`, form)
      await this.fetchTasks()
      return data
    },
    async deleteTask(id) {
      await api.delete(`/tasks/${id}`)
      await this.fetchTasks()
    },

    // Resources
    async fetchResources() {
      const { data } = await api.get('/resources/')
      this.resources = data
    },
    async createResource(form) {
      const { data } = await api.post('/resources/', form)
      await this.fetchResources()
      return data
    },
    async updateResource(id, form) {
      const { data } = await api.put(`/resources/${id}`, form)
      await this.fetchResources()
      return data
    },
    async deleteResource(id) {
      await api.delete(`/resources/${id}`)
      await this.fetchResources()
    },

    // Consumption
    async addConsumption(form) {
      const { data } = await api.post('/resources/consumption', form)
      await this.fetchResources()
      return data
    },
    async fetchConsumptions() {
      const { data } = await api.get('/resources/consumption')
      this.consumptions = data
    },

    // Reports
    async fetchAnalytics() {
      const { data } = await api.get('/reports/analytics')
      this.analytics = data
    },
    async fetchProfitability() {
      const { data } = await api.get('/reports/profitability')
      this.profitability = data
    },
    async createWorkReport(form) {
      const { data } = await api.post('/reports/work', form)
      return data
    },
    async fetchWorkReports(taskId) {
      const { data } = await api.get('/reports/work', { params: { task_id: taskId } })
      this.workReports = data
    },
  },
})
