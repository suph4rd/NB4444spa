<template>
  <div class="main-content">
    <v-card :style="{'width': '100%'}">
      <v-form
        ref="form"
        :style="{'margin': '15px'}"
        @submit.prevent="validForm"
        v-if="obj"
      >

      <v-text-field
        outlined
        v-model="obj.username"
        rows="4"
        label="Логин"
        required
        :rules="[v => !!v] || 'Обязательное поле!'"
      ></v-text-field>

      <v-text-field
        outlined
        v-model="obj.password"
        rows="4"
        label="Пароль"
        required
        type="password"
        :rules="[v => !!v] || 'Обязательное поле!'"
      ></v-text-field>

      <v-text-field
        outlined
        v-model="obj.firstName"
        rows="4"
        label="Имя"
        required
        :rules="[v => !!v] || 'Обязательное поле!'"
      ></v-text-field>

      <v-text-field
        outlined
        v-model="obj.lastName"
        rows="4"
        label="Фамилия"
        required
        :rules="[v => !!v] || 'Обязательное поле!'"
      ></v-text-field>

      <v-text-field
        outlined
        v-model="obj.email"
        rows="4"
        label="Электронная почта"
        required
        type="email"
        :rules="[v => !!v] || 'Обязательное поле!'"
      ></v-text-field>


      <v-btn
        color="success"
        class="mr-4"
        type="submit"
      >Отправить</v-btn>

      <v-btn
        color="danger"
        class="mr-4"
        text
        @click="resetForm"
      >
        Сбросить
      </v-btn>

      <v-btn
        color="secondary"
        :to="{ name: 'Login'}"
      >
        Войти
      </v-btn>

    </v-form>
  </v-card>
  </div>
</template>

<script>
  import header from "../../mixins/header";
  import createMixin from "@/mixins/createMixin";


  export default {
    name: 'UserCreate',
    mixins: [header, createMixin],

    data: function () {
      return {
        defaultObj: {
          password: '',
          firstName: '',
          lastName: '',
          username: '',
          email: '',
        },

        obj: null,

        createPath: '/api/v1/user/',

      }
    },
    methods: {

      getFormParams() {
        return {
            "password": this.obj.password,
            "firstName": this.obj.firstName,
            "lastName": this.obj.lastName,
            "username": this.obj.username,
            "email": this.obj.email,
          }
      },

      preMount(){
        this.obj = Object.assign({}, this.defaultObj);
      },

      validForm(e) {
        this.$refs.form.validate().then((resp) => {
          if (resp.valid) {
            this.sendForm(e);
          }
        })
      },

      redirectLogic(res) {
          alert(`Пользователь ${res.data.username} успешно создан! Пожалуйста авторизуйтесь!`);
          this.$router.push({ name: 'Login'});
      },

      resetForm() {
        this.obj = Object.assign({}, this.defaultObject);
      },

      handleBadRequest(res) {
        alert(JSON.stringify(res.response.data));
        return true
      }

    }
  }
</script>