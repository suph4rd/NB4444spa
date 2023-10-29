<template>
  <div>
      <v-card>
        <h2 class="grey lighten-2 text-center">Обновление плана</h2>
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
                color="primary"
                text
                type="submit"
              >
                Отправить
              </v-btn>
              <v-btn
                color="danger"
                text
                @click="resetForm"
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
  import updateMixin from "../../mixins/updateMixin";

  export default {
    name: "PlanUpdate",
    mixins: [header, updateMixin],

    data () {
      return {
        object: {
          name: '',
        },
        updatePath: '/api/v1/plan/',
      }
    },

    methods: {
      reset () {
        this.$refs.form.reset()
      },

      getFormParams() {
        return {
            "name": this.object.name,
            "user": this.object.user.hasOwnProperty('id') ? this.object.user.id : this.object.user
          }
      },

      resetForm() {
        this.object = Object.assign({}, this.defaultObject);
      },

      getUpdatePath() {
        return `${this.$apiHost}${this.updatePath}${this.$route.params.planId}/`
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