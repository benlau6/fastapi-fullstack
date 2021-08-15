import request from '@/utils/request'

export function login(data) {
  const form = new FormData()
  form.append('username', data.username)
  form.append('password', data.password)
  return request({
    url: '/auth/login/access-token',
    method: 'post',
    data: form
  })
}

export function getInfo() {
  // pass token by authorization headers, which added by service.interceptors.request
  return request({
    url: '/users/me',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/auth/logout',
    method: 'post'
  })
}

export function getUsers(query) {
  let params = {
    'limit': query.limit,
    'skip': (query.page-1) * query.limit,
  }
  if (query.email) {
    params.q = {
      email: query.email
    }
  }

  return request({
    url: '/users/',
    method: 'get',
    params: params
  })
}

export function createUser(data) {
  return request({
    url: '/users/',
    method: 'post',
    data
  })
}

export function updateUser(id, data) {
  return request({
    url: '/users/' + id,
    method: 'patch',
    data
  })
}

export function deleteUser(id) {
  return request({
    url: '/users/' + id,
    method: 'delete'
  })
}
