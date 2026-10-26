import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { CkeditorPlugin } from '@ckeditor/ckeditor5-vue'
import configureAuthInterceptors from './services/authInterceptors'

loadFonts()

const app = createApp(App)
const apiPort = import.meta.env.VITE_API_PORT || '8008'

app.use(router)
app.use(store)
app.use(vuetify)
app.use(VueAxios, axios)

app.use(CkeditorPlugin)
app.config.globalProperties.$apiHost = `http://${document.location.hostname}:${apiPort}`
configureAuthInterceptors(axios, store, router, app.config.globalProperties.$apiHost)

app.mount('#app')