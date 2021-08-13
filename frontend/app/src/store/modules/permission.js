import { asyncRoutes, constantRoutes } from '@/router'

/**
 * Use meta.principal to determine if the current user has permission
 * @param scopes
 * @param route
 */
function hasPermission(scopes, route) {
  if (route.meta && route.meta.scopes) {
    return scopes.some(principal => route.meta.scopes.includes(principal))
  } else {
    return true
  }
}

/**
 * Filter asynchronous routing tables by recursion
 * @param routes asyncRoutes
 * @param scopes
 */
export function filterAsyncRoutes(routes, scopes) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPermission(scopes, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncRoutes(tmp.children, scopes)
      }
      res.push(tmp)
    }
  })

  return res
}

const state = {
  routes: [],
  addRoutes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = constantRoutes.concat(routes)
  }
}

const actions = {
  generateRoutes({ commit }, scopes) {
    return new Promise(resolve => {
      let accessedRoutes
      if (scopes.includes('role:admin')) {
        accessedRoutes = asyncRoutes || []
      } else {
        accessedRoutes = filterAsyncRoutes(asyncRoutes, scopes)
      }
      commit('SET_ROUTES', accessedRoutes)
      resolve(accessedRoutes)
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
