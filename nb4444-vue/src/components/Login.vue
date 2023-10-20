<template>
  <div :style="{'display': 'flex', 'justify-content': 'center'}">
  <v-form
    ref="form"
    v-model="valid"
    lazy-validation
    :style="{'width': '500px'}"
    @submit="login"
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
      login(e) {
          e.preventDefault();
          this.axios.post( `${this.$apiHost}/auth/jwt/create/`, {
            "username": this.username,
            "password": this.password
          }).then((result) =>{
            if (result.status === 200) {
              let userTokens = result.data
              sessionStorage.setItem('user', JSON.stringify(userTokens));
              this.getUserInfo();
            } else {
              sessionStorage.removeItem('user');
              alert("Ошибка отправки запроса!")
            }
        }).catch((res) => {
            if (res.response) {
              alert(`status: ${res.response.status} message: ${res.response.statusText}`)
            }
            console.log(res);
          })
      },

      getUserInfo() {
        let headers = this.getHeaders();
        this.axios.get(`${this.$apiHost}/api/v1/user/current_user/`, {
          headers: headers
        }).then((result) => {
          let userInfo = result.data;
          let userTokens = JSON.parse(sessionStorage.getItem('user', JSON.stringify(userInfo)));
          userInfo = Object.assign(userInfo, userTokens);
          sessionStorage.setItem('user', JSON.stringify(userInfo));
          this.$router.push('/');
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

