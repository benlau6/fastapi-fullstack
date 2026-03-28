import { constantRoutes } from '@/router'

describe('menu chinese labels', () => {
  it('contains four edu menu labels', () => {
    const titles = []
    constantRoutes.forEach(route => {
      if (route.children) {
        route.children.forEach(child => {
          if (child.meta && child.meta.title) {
            titles.push(child.meta.title)
          }
        })
      }
    })
    expect(titles).toContain('学生管理')
    expect(titles).toContain('教师管理')
    expect(titles).toContain('课程管理')
    expect(titles).toContain('班级管理')
  })
})
