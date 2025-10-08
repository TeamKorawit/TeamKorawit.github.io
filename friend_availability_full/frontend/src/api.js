import axios from 'axios'
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'
const api = axios.create({ baseURL: API_BASE })
export const summaryByDate = (params) => api.get('/availabilities/summary_by_date/', { params })
export const exportCsvUrl = (params) => `${API_BASE}/availabilities/export_csv/?${new URLSearchParams(params).toString()}`
export default api
