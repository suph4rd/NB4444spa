<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          aspect-ratio="16/9"
          cover
          src="@/assets/lamborgini.webp"
          width="100%"
          class="rounded"
        ></v-img>
<!--        <img class="rounded" src="../../../media/lambaZel.jpg" width="100%" alt="">-->
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'Main',

    data: function () {
      return {

      }
    }
  }
</script>

<style>
  .actions-btn {
    display: flex;
    justify-content: end;
  }
</style>