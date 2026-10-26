<template>
  <div :style="{'display': 'flex', 'justify-content': 'center'}">
  <v-form
    ref="form"
    v-model="valid"
    validate-on="submit lazy"
    :style="{'width': '500px'}"
    @submit.prevent="login"
  >
    <v-text-field
      v-model="username"
      :rules="nameRules"
      label="Логин"
      required
    ></v-text-field>

    <v-text-field
      v-model="password"
      label="Пароль"
      type="password"
      required
    ></v-text-field>

    <v-btn
      :disabled="!valid"
      color="success"
      class="mr-4"
      type="submit"
    >Вход</v-btn>

    <v-btn
      color="error"
      class="mr-4"
      @click="reset"
    >Сброс</v-btn>

    <v-btn
      color="secondary"
      :to="{ name: 'Registration'}"
    >
      Регистрация
    </v-btn>


  </v-form>
  </div>
</template>

<script>
  import header from "@/mixins/header";

  export default {
    name: 'Login',
    mixins: [header],

    data: () => ({
      valid: true,
      username: '',
      password: '',
      nameRules: [
        v => !!v || 'Username is required',
        v => (v && v.length <= 255) || 'Name must be less than 255 characters',
      ],
    }),

    methods: {
      validate () {
        this.$refs.form.validate()
      },
      login() {
          this.axios.post( `${this.$apiHost}/auth/jwt/create/`, {
            "username": this.username,
            "password": this.password
          }).then((result) =>{
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
