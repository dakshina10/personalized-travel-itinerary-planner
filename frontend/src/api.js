const BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
async function request(path, options={}) {
  const res = await fetch(`${BASE}${path}`, {headers:{'Content-Type':'application/json',...(options.headers||{})},...options})
  if (!res.ok) {
    let message = `Request failed (${res.status})`
    try { const data = await res.json(); message = data.detail || message } catch {}
    throw new Error(message)
  }
  return res.json()
}
export const api = {
  list:()=>request('/api/itineraries'),
  get:id=>request(`/api/itineraries/${id}`),
  generate:data=>request('/api/itineraries/generate',{method:'POST',body:JSON.stringify(data)}),
  update:trip=>request(`/api/itineraries/${trip.id}`,{method:'PUT',body:JSON.stringify({itinerary:trip})}),
  regenerate:id=>request(`/api/itineraries/${id}/regenerate`,{method:'POST'}),
  remove:id=>request(`/api/itineraries/${id}`,{method:'DELETE'})
}
