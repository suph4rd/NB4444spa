// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify
import { createVuetify } from 'vuetify'
import {
  VDataTable,
  VDataTableServer,
  VDataTableVirtual,
} from "vuetify/labs/VDataTable";

export default createVuetify({
        components: {
        VDataTable,
        VDataTableServer,
        VDataTableVirtual,
      },
    }
  // https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
)
