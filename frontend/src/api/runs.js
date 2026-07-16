import api from './client'

export async function getRuns() {
  const { data } = await api.get('/runs/')
  return data
}

export async function getRunDetail(id) {
  const { data } = await api.get(`/runs/${id}`)
  return data
}

export function uploadRun(file) {
  const form = new FormData()
  form.append('file', file)

  return api.post('/runs/upload', form).then((r) => r.data)
}
