import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/potato',
    method: 'get',
    params
  })
}
