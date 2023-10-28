<template>
  <div class="main-content">
    <v-card :style="{'width': '100%'}">
    <v-form
      ref="form"
      lazy-validation
      :style="{'margin': '15px'}"
      @submit.prevent="createNotes"
    >
<!--    <v-textarea-->
<!--      outlined-->
<!--      v-model="text"-->
<!--      rows="4"-->
<!--      label="Сообщение"-->
<!--      required-->
<!--    ></v-textarea>-->

    <div class="mb-5">
      <ckeditor :editor="editor" v-model="text" :config="editorConfig"></ckeditor>
    </div>

    <v-file-input
      label="Файл"
      outlined
      dense
      v-model="image"
    ></v-file-input>

    <v-btn
      color="success"
      class="mr-4"
      type="submit"
    >Отправить</v-btn>
  </v-form>
  </v-card>
  </div>
</template>

<script>
  import header from "../../mixins/header";
  import ClassicEditor from "@ckeditor/ckeditor5-build-classic";

  export default {
    name: 'NoteCreate',
    mixins: [header],
    components: {ClassicEditor},

    data: function () {
      return {
        "text": "",
        "image": null,
        "fileval": null,

        editor: ClassicEditor,
        editorConfig: {},

      }
    },
    methods: {

      createNotes(e) {
          if (!this.text && !this.image) {
            alert("Форма пуста!");
            return;
          }
          let data;
          let headers = this.getHeaders();
          if (this.image) {
            let formData = new FormData()
            formData.append("text", this.text);
            formData.append("image",  this.image[0], this.image[0].name);
            data = formData;
            headers['Content-Type'] = 'multipart/form-data';
          } else {
            data = {
              "text": this.text,
            }
          }
          this.axios.post(`${this.$apiHost}/api/v1/note/`, data, {
            headers: headers
          }).then((result) =>{
            this.image = null;
            this.text = '';
            this.$emit("onCreate");
        }).catch((res) => {
            this.dropSession(res);
        })
      },

    }
  }
</script>