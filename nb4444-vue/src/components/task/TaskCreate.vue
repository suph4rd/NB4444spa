<template>
  <div>

      <v-card>
        <h2 class="grey lighten-2 text-center">Создание задачи</h2>
          <v-form
            v-if="object"
            ref="form"
            @submit.prevent="validForm"
            :style="{'margin': '15px'}"
          >
            <v-text-field
              type="text"
              v-model="object.plan.name"
              label="Название плана"
              disabled
            ></v-text-field>

            <v-select
              label="Select"
              :items="priorityList"
              v-model="object.priority"
              item-title="key"
              item-value="val"
            ></v-select>

<!--            <v-textarea-->
<!--              outlined-->
<!--              v-model="object.description"-->
<!--              rows="4"-->
<!--              label="Описание"-->
<!--              :rules="[v => !!v] || 'Обязательное поле!'"-->
<!--              required-->
<!--            >-->
<!--            </v-textarea>-->

            <div class="mb-5">
              <ckeditor :editor="editor" v-model="object.description" :config="editorConfig"></ckeditor>
            </div>

            <v-select
              v-model="object.section"
              :items="sections"
              label="Секция"
              item-title="name"
              item-value="id"
              :rules="[v => !!v] || 'Обязательное поле!'"
              required
            ></v-select>

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
                @click="resetForm"
              >
                Сбросить
              </v-btn>
              <v-btn
                color="secondary"
                text
                :to="{ name: 'PlanDetail', params: {planId: this.$route.params.planId} }"
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
  import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

  export default {
    name: "TaskCreate",
    mixins: [header, createMixin],
    components: {ClassicEditor},

    data () {
      return {
        sections: [],
        object: null,
        priorityList: [
          {key: "Low", val: 0},
          {key: "Medium", val: 1},
          {key: "High", val: 2},
          {key: "Hot", val: 3},
        ],
        objectDefault: {
          plan:'',
          section: '',
          description: '',
          priority: 1,
        },
        createPath: '/api/v1/task/',

        editor: ClassicEditor,
        editorConfig: {},

      }
    },
    methods: {

      getSections() {
        let headers = this.getHeaders();
        this.axios.get(`${this.$apiHost}/api/v1/section-list/`, {
          headers: headers
        }).then((result) =>{
          console.log(result.data)
          this.sections = result.data;
        }).catch((res) => {
            this.dropSession(res);
        })
      },

      getPlan() {
        let headers = this.getHeaders();
        this.axios.get(`${this.$apiHost}/api/v1/plan/${this.$route.params.planId}/`, {
          headers: headers
        }).then((result) =>{
          console.log(result.data);
          this.objectDefault.plan = result.data;
          this.object = Object.assign({}, this.objectDefault);
        }).catch((res) => {
            this.dropSession(res);
        });
      },

      getFormParams() {
        return {
            "plan": this.$route.params.planId,
            "section": this.object.section,
            "description": this.object.description,
            "priority": this.object.priority,
          }
      },

      validForm(e) {
        this.$refs.form.validate().then((resp) => {
          if (resp.valid) {
            this.sendForm(e);
          }
        })
      },

      preMount() {
        this.getPlan();
        this.getSections();
      },

      redirectLogic() {
          this.$router.push({ name: 'PlanDetail', params: {planId: this.$route.params.planId}});
      },

      resetForm() {
        this.object = Object.assign({}, this.objectDefault);
      },

    },

  }
</script>