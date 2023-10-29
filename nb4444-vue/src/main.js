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

let app = createApp(App)

app.use(router)
app.use(store)
app.use(vuetify)
app.use(VueAxios, axios)
app.use(CKEditor)
// app.config.globalProperties.$apiHost = `http://${document.location.hostname}:8008` // for dev
app.config.globalProperties.$apiHost = `http://${document.location.hostname}:9999` // for prod

app.mount('#app')