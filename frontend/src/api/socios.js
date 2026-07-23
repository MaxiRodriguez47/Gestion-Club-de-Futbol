import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const getSocios = () => api.get('/socios/')
export const getSocio = (id) => api.get(`/socios/${id}`)
export const createSocio = (data) => api.post('/socios/', data)
export const updateSocio = (id, data) => api.put(`/socios/${id}`, data)
export const deleteSocio = (id) => api.delete(`/socios/${id}`)
