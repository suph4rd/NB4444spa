import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import axios from 'axios'
import VueAxios from 'vue-axios'

loadFonts()

let app = createApp(App)

app.use(router)
app.use(store)
app.use(vuetify)
app.use(VueAxios, axios)

app.config.globalProperties.$apiHost = 'http://0.0.0.0:8008' // for dev
// app.config.globalProperties.$apiHost = 'http://0.0.0.0:9009' // for prod
// app.config.globalProperties.$apiHost = 'http://nb4_api_prod:8008' // for prod

app.mount('#app')