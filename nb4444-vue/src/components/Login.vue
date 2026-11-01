<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div class="login-page">
          <v-card class="login-card" color="surface" elevation="8">
            <v-card-title class="text-center">Вход</v-card-title>
            <v-card-text>
              <v-form
                ref="form"
                validate-on="submit lazy"
                @submit.prevent="login"
              >
                <v-text-field
                  v-model="username"
                  :rules="nameRules"
                  label="Логин"
                  autocomplete="username"
                  required
                ></v-text-field>

                <v-text-field
                  v-model="password"
                  :rules="passwordRules"
                  label="Пароль"
                  type="password"
                  autocomplete="current-password"
                  required
                ></v-text-field>

                <div class="login-actions">
                  <v-btn color="success" type="submit">Вход</v-btn>
                  <v-btn color="error" variant="outlined" @click="reset">Сброс</v-btn>
                  <v-btn color="secondary" :to="{ name: 'Registration' }">
                    Регистрация
                  </v-btn>
                </div>
              </v-form>
            </v-card-text>
          </v-card>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import header from '@/mixins/header'

  export default {
    name: 'Login',
    mixins: [header],

    data: () => ({
      username: '',
      password: '',
      nameRules: [
        value => !!value || 'Введите логин',
        value => value.length <= 255 || 'Логин должен быть не длиннее 255 символов',
      ],
      passwordRules: [value => !!value || 'Введите пароль'],
    }),

    methods: {
      async login() {
        const { valid } = await this.$refs.form.validate()
        if (!valid) {
          return
        }

        this.axios.post(`${this.$apiHost}/auth/jwt/create/`, {
          username: this.username,
          password: this.password,
        }).then((result) => {
          if (!result.data || !result.data.access) {
            throw new Error('The authentication response did not contain an access token.')
          }
          this.$store.commit('setUser', result.data)
          this.getUserInfo()
        }).catch((res) => {
          if (res.response) {
            alert(`status: ${res.response.status} message: ${res.response.statusText}`)
          }
          console.error(res)
        })
      },

      getUserInfo() {
        let headers = this.getHeaders();
        this.axios.get(`${this.$apiHost}/api/v1/user/current_user/`, {
          headers: headers
        }).then((result) => {
          const userInfo = Object.assign({}, this.$store.state.user, result.data)
          this.$store.commit('setUser', userInfo)

          const redirect = this.$route.query.redirect
          const destination = typeof redirect === 'string'
            && redirect.startsWith('/')
            && !redirect.startsWith('//')
            ? redirect
            : { name: 'Main' }
          this.$router.replace(destination)
        }).catch((res) => {
            this.dropSession(res);
            alert("Не удалось получить информацию о пользователе!!");
        })
      },

      reset () {
        this.$refs.form.reset()
      },
    },
  }
</script>

<style>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
}

.login-card {
  width: min(100%, 500px);
}

.login-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 8px;
}
</style>
