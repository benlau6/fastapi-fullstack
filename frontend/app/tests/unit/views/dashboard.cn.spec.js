import { shallowMount } from '@vue/test-utils'
import Dashboard from '@/views/dashboard/index.vue'

describe('dashboard chinese content', () => {
  it('renders chinese dashboard text', () => {
    const wrapper = shallowMount(Dashboard, {
      computed: {
        name: () => '管理员',
        scopes: () => ['role:admin']
      }
    })
    expect(wrapper.text()).toContain('欢迎')
    expect(wrapper.text()).toContain('权限列表')
  })
})
