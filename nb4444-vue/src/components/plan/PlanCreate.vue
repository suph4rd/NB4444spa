<template>
  <div>
      <v-card>
        <h2 class="grey lighten-2 text-center">Создание плана</h2>
          <v-form
            ref="form"
            @submit.prevent="validForm"
            :style="{'margin': '15px'}"
          >
            <v-text-field
              type="text"
              v-model="object.name"
              label="Название плана"
              :rules="[v => !!v] || 'Обязательное поле!'"
              required
            ></v-text-field>

            <v-divider></v-divider>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="success"
                text
                type="submit"
              >
                Создать
              </v-btn>
              <v-btn
                color="danger"
                text
                @click="reset"
              >
                Сбросить
              </v-btn>
              <v-btn
                color="secondary"
                text
                :to="{ name: 'PlanList'}"
              >
                Назад
              </v-btn>
            </v-card-actions>
        </v-form>
      </v-card>
  </div>
</template>

<script>
  import header from "../../mixins/header";
  import createMixin from "../../mixins/createMixin";

  export default {
    name: "PlanCreate",
    mixins: [header, createMixin],

    data () {
      return {
        users: [],
        object: {
          name: '',
          user: '',
        },
        createPath: '/api/v1/plan/',
      }
    },
    methods: {
      reset () {
        this.$refs.form.reset()
      },

      getFormParams() {
        let user = JSON.parse(sessionStorage.getItem('user'));
        return {
            "name": this.object.name,
            "user": user.id,
          }
      },

      resetForm() {
        this.reset();
      },

      validForm(e) {
        this.$refs.form.validate().then((resp) => {
          if (resp.valid) {
            this.sendForm(e);
          }
        })
      },

      redirectLogic (res) {
        this.$router.push({ name: 'PlanList'});
      },

    },
  }
</script>