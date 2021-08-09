import { asyncRoutes, constantRoutes } from '@/router'

/**
 * Use meta.principal to determine if the current user has permission
 * @param principals
 * @param route
 */
function hasPermission(principals, route) {
  if (route.meta && route.meta.principals) {
    return principals.some(principal => route.meta.principals.includes(principal))
  } else {
    return true
  }
}

/**
 * Filter asynchronous routing tables by recursion
 * @param routes asyncRoutes
 * @param principals
 */
export function filterAsyncRoutes(routes, principals) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPermission(principals, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncRoutes(tmp.children, principals)
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
  generateRoutes({ commit }, principals) {
    return new Promise(resolve => {
      let accessedRoutes
      if (principals.includes('role:admin')) {
        accessedRoutes = asyncRoutes || []
      } else {
        accessedRoutes = filterAsyncRoutes(asyncRoutes, principals)
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
