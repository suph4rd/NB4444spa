<template>
  <div class="main-content">
    <v-card :style="{'width': '100%'}">
    <v-form
      ref="form"
      lazy-validation
      :style="{'margin': '15px'}"
      @submit.prevent="updateNotes"
      v-if="object"
    >
    <v-textarea
      outlined
      v-model="object.text"
      rows="4"
      label="Сообщение"
      required
    ></v-textarea>

    <v-checkbox
      v-model="dropFile"
      label="Удалить файл"
      color="success"
    ></v-checkbox>

    <v-img v-if="object.image" :src="object.image"></v-img>

    <v-file-input
      label="Файл"
      outlined
      dense
      v-model="newImage"
      class="mt-5"
    ></v-file-input>

    <div class="row">

        <v-btn
          color="success"
          class="col btn-action"
          type="submit"
        >Отправить</v-btn>

        <v-btn
          class="col btn-action"
          @click="resetForm"
          color="secondary"
        >Сброс</v-btn>

        <div class="col btn-action" style="display: inline-block" >
          <Delete
            @onDelete="redirectLogic"
            :objId="object.id"
            :deletePath="'/api/v1/note/'"
            :titleDelete="'заметки'"
            :messageDelete="'заметку'"
            :is-simple="true"
          >
          </Delete>
        </div>

        <v-btn
          class="col btn-action"
          :to="{ name: 'Note'}"
        >
          Назад
        </v-btn>

      </div>

  </v-form>
  </v-card>
  </div>
</template>

<script>
  import header from "../../mixins/header";
  import Delete from "@/components/common_components/Delete.vue";

  export default {
    name: 'NoteUpdate',
    components: {Delete},
    mixins: [header],

    data: function () {
      return {
        newImage: null,
        defaultObject: null,
        dropFile: false,
        object: {
          text: "",
          image: null,
        },
      }
    },
    methods: {

      updateNotes() {
          if (!this.object.text && !this.object.image) {
            alert("Форма пуста!");
            return;
          }
          let data;
          let headers = this.getHeaders();
          if (this.newImage) {
            let formData = new FormData()
            formData.append("text", this.object.text);
            formData.append("image",  this.newImage[0], this.newImage[0].name);
            data = formData;
            headers['Content-Type'] = 'multipart/form-data';
          } else {
            data = {
              "text": this.object.text,
            }
            if (this.dropFile) {
              data['image'] = null;
            }
          }
          this.axios.patch(`${this.$apiHost}/api/v1/note/${this.$route.params.noteId}/`, data, {
            headers: headers
          }).then((result) =>{
            this.redirectLogic();
        }).catch((res) => {
            this.dropSession(res);
        })
      },

      getObject() {
        let headers = this.getHeaders();
        this.axios.get(`${this.$apiHost}/api/v1/note/${this.$route.params.noteId}/`, {
          headers: headers
        }).then((result) =>{
          console.log(result.data);
          this.defaultObject = result.data;
          this.object = Object.assign({}, this.defaultObject);
        }).catch((res) => {
            this.dropSession(res);
        });
      },

      redirectLogic () {
        this.$router.push({ name: 'Note'});
      },

      resetForm() {
        this.object = Object.assign({}, this.defaultObject);
        this.newImage = null;
      },


    },

    mounted() {
      this.getObject();
    },
  }
</script>

<style scoped>
  .btn-action {
    margin: 10px
  }
</style>