<template>
  <div class="main-content">
    <v-card :style="{'width': '100%'}">
    <v-form
      ref="form"
      lazy-validation
      :style="{'margin': '15px'}"
      @submit.prevent="createNotes"
    >
    <v-textarea
      outlined
      v-model="text"
      rows="4"
      label="Сообщение"
      required
    ></v-textarea>

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

  export default {
    name: 'NoteCreate',
    mixins: [header],

    data: function () {
      return {
        "text": "",
        "image": null,
        "fileval": null
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