import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const getPartidos = () => api.get('/partidos/')
export const getPartido = (id) => api.get(`/partidos/${id}`)
export const createPartido = (data) => api.post('/partidos/', data)
export const updatePartido = (id, data) => api.put(`/partidos/${id}`, data)
export const deletePartido = (id) => api.delete(`/partidos/${id}`)
