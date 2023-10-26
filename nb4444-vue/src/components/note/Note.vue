<template>
  <v-container>
    <h1 class="text-center">Заметки</h1>
    <NoteCreate :style="{'margin-bottom': '70px'}" @onCreate="getData" />
    <v-text-field
      v-if="!objects"
      color="success"
      loading
      disabled
    ></v-text-field>

    <v-pagination
        v-if="objects"
        v-model="page"
        :length="Math.floor(objects.length / 10)"
        class="mb-10"
      ></v-pagination>

    <div v-for="(item, index) in objects">
      <v-card v-if="index + 1 <= page * 10 && (page === 1 || index >= page * 10 - 10)" class="mb-5" >
        <v-card-text>
          <div>{{index + 1}}. {{item.user.username}}</div>
          <div><span class="font-weight-bold">{{ item.created_at }}</span> <span v-html="item.text" /></div>
        </v-card-text>
        <v-img v-if="item.image" :src="item.image"></v-img>
        <v-btn :to="{ name: 'NoteUpdate', params: {noteId: item.id} }" class="mt-5 ml-5 mb-5">
            Изменить
          </v-btn>
      </v-card>
    </div>

    <v-pagination
        v-if="objects"
        v-model="page"
        :length="Math.floor(objects.length / 10)"
      ></v-pagination>

  </v-container>
</template>

<script>
  import header from "../../mixins/header";
  import NoteCreate from "./NoteCreate";
  import listMixin from "../../mixins/listMixin";

  export default {
    name: 'Note',
    mixins: [header, listMixin],
    components: {NoteCreate},

    data: function () {
      return {
        objects: null,
        apiPath: "/api/v1/note/",
        page: 1,
      }
    },
  }
</script>
