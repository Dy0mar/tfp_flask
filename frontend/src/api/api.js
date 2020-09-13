import axios from 'axios'

const url = '/api/'

const instance = axios.create({
  baseURL: url,
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json'
  },
})

instance.interceptors.request.use(
  function (config) {
    const token = localStorage.getItem("token")
    if (token)
      config.headers.Authorization = `Bearer ${token}`
    return config
  },
  function (error) {
    return Promise.reject (error)
  }
)

export const api = {
  get_user_list() {
    return instance.get('users/')
      .then(r => r.data)
      .catch(e => e.response.data)
  },
  get_access(email){
    return instance.post('get-access/', {email: email})
      .then(r => r.data)
  },
  set_access(id){
    return instance.get('set-access/'+id)
      .then(r => r.data)
  },
  confirm(token){
    return instance.get('confirm/?token='+token)
      .then(r => r.data)
      .catch(e => e.response.data)
  },
  delete(userId){
    return instance.delete('delete/'+userId)
      .then(r => r.data)
      .catch(e => e.response.data)
  },
}