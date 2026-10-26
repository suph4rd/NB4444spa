function redirectToLogin(router) {
  const currentRoute = router.currentRoute.value
  if (currentRoute.name !== 'Login') {
    router.replace({
      name: 'Login',
      query: { redirect: currentRoute.fullPath },
    })
  }
}

export default function configureAuthInterceptors(axios, store, router, apiHost) {
  let refreshRequest = null

  axios.interceptors.request.use((config) => {
    const accessToken = store.state.user && store.state.user.access
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }
    return config
  })

  axios.interceptors.response.use(
    response => response,
    async (error) => {
      const request = error.config
      const requestUrl = (request && request.url) || ''
      if (
        !request
        || !error.response
        || error.response.status !== 401
        || request._authRetried
        || requestUrl.includes('/auth/jwt/create/')
        || requestUrl.includes('/auth/jwt/refresh/')
      ) {
        return Promise.reject(error)
      }

      const user = store.state.user
      if (!user) {
        return Promise.reject(error)
      }

      if (!user.refresh) {
        store.commit('clearUser')
        redirectToLogin(router)
        return Promise.reject(error)
      }

      const refreshToken = user.refresh
      request._authRetried = true
      if (!refreshRequest) {
        refreshRequest = axios.post(`${apiHost}/auth/jwt/refresh/`, {
          refresh: refreshToken,
        }).then((response) => {
          if (!response.data || !response.data.access) {
            store.commit('clearUser')
            redirectToLogin(router)
            throw new Error('The token refresh response did not contain an access token.')
          }

          const currentUser = store.state.user
          if (!currentUser || currentUser.refresh !== refreshToken) {
            throw new Error('The user session changed while refreshing the token.')
          }

          store.commit('setUser', {
            ...currentUser,
            ...response.data,
          })
          return response.data.access
        }).catch((refreshError) => {
          const status = refreshError.response && refreshError.response.status
          if (status === 400 || status === 401) {
            store.commit('clearUser')
            redirectToLogin(router)
          }
          throw refreshError
        }).finally(() => {
          refreshRequest = null
        })
      }

      try {
        const accessToken = await refreshRequest
        request.headers = request.headers || {}
        request.headers.Authorization = `Bearer ${accessToken}`
        return axios(request)
      } catch (refreshError) {
        return Promise.reject(refreshError)
      }
    },
  )
}
