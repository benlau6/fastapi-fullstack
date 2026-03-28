describe('message chinese text coverage', () => {
  it('includes chinese error messages in request interceptor', () => {
    const source = require('fs').readFileSync(require('path').resolve(__dirname, '../../../src/utils/request.js'), 'utf8')
    expect(source).toContain('无权限访问')
    expect(source).toContain('数据冲突，请检查唯一字段')
    expect(source).toContain('参数校验失败，请检查输入')
    expect(source).toContain('登录已失效，请重新登录')
  })
})
