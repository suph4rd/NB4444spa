<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          aspect-ratio="16/9"
          cover
          :src="mainImage"
          width="100%"
          class="rounded"
          alt="Зелёный автомобиль"
        ></v-img>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import mainImage from '@/assets/lamborgini.webp'

  export default {
    name: 'Main',

    data: function () {
      return {
        mainImage,
      }
    }
  }
</script>