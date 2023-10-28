<template>
  <div>

      <v-card>
        <h2 class="grey lighten-2 text-center">Обновление задачи</h2>
          <v-form
            ref="form"
            @submit.prevent="validForm"
            :style="{'margin': '15px'}"
          >
            <v-checkbox
              v-model="object.is_ready"
              label="Готово"
              color="success"
            ></v-checkbox>

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
<!--            ></v-textarea>-->

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
  import updateMixin from "../../mixins/updateMixin";
  import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

  export default {
    name: "TaskUpdate",
    mixins: [header, updateMixin],
    components: {ClassicEditor},

    data () {
      return {
        sections: [],
        priorityList: [
          {key: "Low", val: 0},
          {key: "Medium", val: 1},
          {key: "High", val: 2},
          {key: "Hot", val: 3},
        ],
        object: {
          plan:'',
          section: '',
          description: '',
          is_ready: false,
          priority: 1,
        },
        updatePath: '/api/v1/task/',

        editor: ClassicEditor,
        editorConfig: {},

      }
    },
    methods: {

      reset () {
        this.$refs.form.reset()
      },

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

      getFormParams() {
        return {
            "plan": this.object.plan.id,
            "section": this.object.section.hasOwnProperty('id') ? this.object.section.id : this.object.section,
            "description": this.object.description,
            "is_ready": this.object.is_ready,
            "priority": this.object.priority,
          }
      },

      resetForm() {
        this.object = Object.assign({}, this.defaultObject);
      },

      getUpdatePath() {
        return `${this.$apiHost}${this.updatePath}${this.$route.params.taskId}/`
      },

      preMount() {
        this.getObject();
        this.getSections();
      },

      validForm(e) {
        this.$refs.form.validate().then((resp) => {
          if (resp.valid) {
            this.sendForm(e);
          }
        })
      },

      redirectLogic () {
        this.$router.push({ name: 'PlanDetail', params: {planId: this.$route.params.planId}});
      },

    },

  }
</script>