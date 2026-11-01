<template>
  <div class="main-content">
    <v-card :style="{'width': '100%'}">
    <v-form
      ref="form"
      validate-on="submit lazy"
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
      <NoteEditor v-model="text" />
    </div>

    <v-file-input
      label="Файл"
      variant="outlined"
      density="compact"
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
  import NoteEditor from "./NoteEditor.vue";

  export default {
    name: 'NoteCreate',
    components: {NoteEditor},
    mixins: [header],
    data: function () {
      return {
        "text": "",
        "image": null,


      }
    },
    methods: {

      createNotes() {
          const image = Array.isArray(this.image) ? this.image[0] : this.image;
          if (!this.text && !image) {
            alert("Форма пуста!");
            return;
          }
          let data;
          let headers = this.getHeaders();
          if (image) {
            let formData = new FormData()
            formData.append("text", this.text);
            formData.append("image", image, image.name);
            data = formData;
            delete headers['Content-Type'];
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