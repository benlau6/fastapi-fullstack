const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  name: state => state.user.name,
  principals: state => state.user.principals,
  permission_routes: state => state.permission.routes
}
export default getters
