// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Vuetify
import { createVuetify } from 'vuetify'
import { VDataTable } from 'vuetify/components'

export default createVuetify({
  theme: {
    defaultTheme: 'system',
    themes: {
      light: {
        colors: {
          primary: '#00C853',
          'on-primary': '#00210B',
          background: '#ECEFF1',
          'on-background': '#1A1C1E',
        },
      },
      dark: {
        colors: {
          primary: '#164B32',
          'on-primary': '#D0F5DE',
          background: '#212121',
          'on-background': '#E6E6E6',
        },
      },
    },
  },
  components: {
    VDataTable,
  },
})
