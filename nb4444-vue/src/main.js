import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import axios from 'axios'
import VueAxios from 'vue-axios'
import CKEditor from '@ckeditor/ckeditor5-vue';

loadFonts()

const app = createApp(App)
const apiPort = process.env.VUE_APP_API_PORT || '8008'

app.use(router)
app.use(store)
app.use(vuetify)
app.use(VueAxios, axios)

app.use(CKEditor)
app.config.globalProperties.$apiHost = `http://${document.location.hostname}:${apiPort}`

app.mount('#app')