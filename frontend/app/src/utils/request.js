import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests e.g. if you are not using reverse-proxy
  timeout: 5000 // request timeout
})

// not needed since cookie is used
// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent
    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      config.headers['Authorization'] = 'Bearer ' + getToken()
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const hasData = response.data != null
    if (hasData && response.data.code !== undefined) {
      return response.data
    }
    return {
      code: 0,
      message: 'ok',
      data: response.data
    }
  },
  error => {
    const status = error.response ? error.response.status : 500
    if (status === 401) {
      MessageBox.confirm('登录已失效，请重新登录', '会话过期', {
        confirmButtonText: '重新登录',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        store.dispatch('user/resetToken').then(() => {
          location.reload()
        })
      })
    } else if (status === 403) {
      Message({ message: '无权限访问', type: 'error', duration: 3000 })
    } else if (status === 409) {
      Message({ message: '数据冲突，请检查唯一字段', type: 'error', duration: 3000 })
    } else if (status === 422) {
      Message({ message: '参数校验失败，请检查输入', type: 'error', duration: 3000 })
    } else {
      Message({ message: error.message, type: 'error', duration: 3000 })
    }
    return Promise.reject(error)
  }
)

export default service
