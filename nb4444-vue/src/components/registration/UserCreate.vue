<template>
  <div class="main-content">
    <v-card :style="{ width: '100%' }">
      <v-card-title class="text-center">Регистрация</v-card-title>
      <v-card-text>
        <v-form
          ref="form"
          validate-on="submit lazy"
          :style="{ margin: '15px' }"
          @submit.prevent="submitForm"
        >
          <v-alert
            v-if="errorMessage"
            type="error"
            role="alert"
            class="mb-4"
          >
            {{ errorMessage }}
          </v-alert>

          <v-text-field
            v-model="obj.username"
            variant="outlined"
            label="Логин"
            autocomplete="username"
            required
            :rules="usernameRules"
            :disabled="submitting"
          ></v-text-field>

          <v-text-field
            v-model="obj.password"
            variant="outlined"
            label="Пароль"
            type="password"
            autocomplete="new-password"
            required
            :rules="passwordRules"
            :disabled="submitting"
          ></v-text-field>

          <v-text-field
            v-model="obj.first_name"
            variant="outlined"
            label="Имя"
            autocomplete="given-name"
            required
            :rules="nameRules"
            :disabled="submitting"
          ></v-text-field>

          <v-text-field
            v-model="obj.last_name"
            variant="outlined"
            label="Фамилия"
            autocomplete="family-name"
            required
            :rules="nameRules"
            :disabled="submitting"
          ></v-text-field>

          <v-text-field
            v-model="obj.email"
            variant="outlined"
            label="Электронная почта"
            type="email"
            autocomplete="email"
            required
            :rules="emailRules"
            :disabled="submitting"
          ></v-text-field>

          <div class="d-flex flex-wrap ga-3">
            <v-btn
              color="success"
              type="submit"
              :loading="submitting"
              :disabled="submitting"
            >
              Зарегистрироваться
            </v-btn>

            <v-btn
              color="error"
              variant="text"
              type="button"
              :disabled="submitting"
              @click="resetForm"
            >
              Сбросить
            </v-btn>

            <v-btn
              color="secondary"
              type="button"
              :to="{ name: 'Login' }"
              :disabled="submitting"
            >
              Войти
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
  import header from '@/mixins/header'

  const createEmptyForm = () => ({
    username: '',
    password: '',
    first_name: '',
    last_name: '',
    email: '',
  })

  const fieldLabels = {
    username: 'Логин',
    password: 'Пароль',
    first_name: 'Имя',
    last_name: 'Фамилия',
    email: 'Электронная почта',
    non_field_errors: 'Ошибка',
    detail: 'Ошибка',
  }

  export default {
    name: 'UserCreate',
    mixins: [header],

    data: () => ({
      obj: createEmptyForm(),
      createPath: '/api/v1/user/',
      submitting: false,
      errorMessage: '',
      usernameRules: [value => !!value?.trim() || 'Введите логин'],
      passwordRules: [
        value => !!value || 'Введите пароль',
        value => value.length >= 8 || 'Пароль должен содержать не менее 8 символов',
      ],
      nameRules: [value => !!value?.trim() || 'Заполните это поле'],
      emailRules: [
        value => !!value?.trim() || 'Введите электронную почту',
        value => !value || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) || 'Введите корректный адрес электронной почты',
      ],
    }),

    methods: {
      getFormParams() {
        return { ...this.obj }
      },

      async submitForm() {
        if (this.submitting) {
          return
        }

        this.submitting = true
        this.errorMessage = ''

        try {
          const { valid } = await this.$refs.form.validate()
          if (!valid) {
            return
          }

          let response
          try {
            response = await this.axios.post(
              `${this.$apiHost}${this.createPath}`,
              this.getFormParams(),
              { headers: this.getHeaders() },
            )
          } catch (error) {
            this.errorMessage = this.getApiErrorMessage(error)
            if (!error?.response) {
              console.error(error)
            }
            return
          }

          alert(`Пользователь ${response.data.username} успешно создан! Пожалуйста авторизуйтесь!`)
          await this.$router.push({ name: 'Login' })
        } finally {
          this.submitting = false
        }
      },

      getApiErrorMessage(error) {
        const responseData = error?.response?.data
        if (responseData && typeof responseData === 'object') {
          const messages = Object.entries(responseData)
            .map(([field, fieldErrors]) => {
              const label = fieldLabels[field] || field
              const message = Array.isArray(fieldErrors) ? fieldErrors.join(' ') : String(fieldErrors)
              return `${label}: ${message}`
            })
          if (messages.length) {
            return messages.join('\n')
          }
        }

        return 'Не удалось создать пользователя. Проверьте соединение и попробуйте ещё раз.'
      },

      resetForm() {
        this.obj = createEmptyForm()
        this.errorMessage = ''
        this.$nextTick(() => this.$refs.form?.resetValidation())
      },
    },
  }
</script>
