<template>
  <div>
    <v-dialog
      v-model="dialogDelete"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
          <v-btn icon @click="showDeleteDialog" v-if="!isSimple">
            <v-icon
              class="mr-2"
            >
              mdi-delete
            </v-icon>
          </v-btn>
          <v-btn @click="showDeleteDialog" v-if="isSimple" color="error">
            удалить
          </v-btn>
      </template>

      <v-card>
        <h2 class="grey lighten-2 text-center mb-5">Удаление {{ titleDelete }}
        </h2>
            <v-card-text>
              Вы действительно хотете удалить {{ messageDelete }}?
            </v-card-text>
            <v-divider></v-divider>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                text
                type="submit"
                @click="sendDeleteForm"
              >
                Удалить
              </v-btn>
              <v-btn
                color="secondary"
                text
                @click="dialogDelete = false"
              >
                Отмена
              </v-btn>
            </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  import header from "../../mixins/header";

  export default {
    name: "Delete",
    mixins: [header],
    props: ['objId', 'deletePath', 'messageDelete', 'titleDelete', 'isSimple'],

    data () {
      return {
        dialogDelete: false,
      }
    },
    methods: {
      getDeletePath() {
        return `${this.$apiHost}${this.$props.deletePath}${this.$props.objId}/`
      },
      showDeleteDialog() {
        this.dialogDelete = true;
      },
      sendDeleteForm(e) {
        e.preventDefault();
        let headers = this.getHeaders();
          this.axios.delete(this.getDeletePath(), {
              headers: headers
            }).then((res) => {
                this.dialogDelete = false;
                this.$emit('onDelete');
            }).catch((res) => {
            this.dropSession(res);
          });
      },
    },
  }
</script>