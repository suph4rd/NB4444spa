import { createStore } from 'vuex'

function loadUser() {
  const storedUser = sessionStorage.getItem('user')

  if (!storedUser) {
    return null
  }

  try {
    const user = JSON.parse(storedUser)
    if (user && typeof user.access === 'string' && user.access) {
      return user
    }
  } catch (error) {
    console.error('Could not restore the saved user session.', error)
  }

  sessionStorage.removeItem('user')
  return null
}

export default createStore({
  state: {
    user: loadUser(),
  },
  getters: {
    isAuthenticated: state => Boolean(state.user && state.user.access),
  },
  mutations: {
    setUser(state, user) {
      state.user = user
      sessionStorage.setItem('user', JSON.stringify(user))
    },
    clearUser(state) {
      state.user = null
      sessionStorage.removeItem('user')
    },
  },
  actions: {},
  modules: {},
})
