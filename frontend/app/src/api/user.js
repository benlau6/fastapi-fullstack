import request from '@/utils/request'

export function login(data) {
  const form = new FormData()
  form.append('username', data.username)
  form.append('password', data.password)
  return request({
    url: '/auth/jwt/login',
    method: 'post',
    data: form
  })
}

export function getInfo() {
  return request({
    url: '/users/me',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/auth/cookie/logout',
    method: 'post'
  })
}

export function getUsers() {
  return request({
    url: '/users',
    method: 'get'
  })
}

export function createUser(data) {
  return request({
    url: '/users',
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
    url: '/users' + id,
    method: 'delete'
  })
}
