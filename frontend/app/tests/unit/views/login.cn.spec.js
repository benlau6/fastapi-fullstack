import { shallowMount } from '@vue/test-utils'
import Login from '@/views/login/index.vue'

describe('login chinese content', () => {
  it('renders chinese title and button', () => {
    const wrapper = shallowMount(Login, {
      mocks: {
        $store: { dispatch: () => Promise.resolve() },
        $router: { push: () => {} },
        $route: { query: {} }
      },
      stubs: ['el-form', 'el-form-item', 'el-input', 'el-button', 'svg-icon']
    })
    expect(wrapper.html()).toContain('教务管理系统登录')
    expect(wrapper.html()).toContain('登录')
  })
})
