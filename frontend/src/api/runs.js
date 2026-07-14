import api from './client'

export async function getRuns() {
  const { data } = await api.get('/runs/')
  return data
}

export async function getRunDetail(id) {
  const { data } = await api.get(`/runs/${id}`)
  return data
}
