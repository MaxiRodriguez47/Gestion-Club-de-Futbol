import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const getJugadores = () => api.get('/jugadores/')
export const getJugador = (id) => api.get(`/jugadores/${id}`)
export const createJugador = (data) => api.post('/jugadores/', data)
export const updateJugador = (id, data) => api.put(`/jugadores/${id}`, data)
export const deleteJugador = (id) => api.delete(`/jugadores/${id}`)
