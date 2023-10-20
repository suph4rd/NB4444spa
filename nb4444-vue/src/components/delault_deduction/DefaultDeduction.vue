<template>
  <v-container>
    <div class="main-content">
      <h1 class="text-center">Стандартные вычеты</h1>
    <v-form
      ref="form"
      :style="{'width': '95%'}"
      v-if="objects"
      @submit="sendDefaultDeductions"
    >
    <v-text-field
      type="number"
      v-model="objects.house"
      label="Дом"
      required
    ></v-text-field>
      <v-text-field
      type="number"
      v-model="objects.travel"
      label="Путешествия"
      required
    ></v-text-field>
      <v-text-field
      type="number"
      v-model="objects.phone"
      label="Телефон"
      required
    ></v-text-field>
      <v-text-field
      type="number"
      v-model="objects.food"
      label="Еда"
      required
    ></v-text-field>
    <v-text-field
      type="number"
      v-model="totalCount"
      label="Итого"
      disabled
    ></v-text-field>

    <v-btn
      color="success"
      class="mr-4"
      type="submit"
    >Отправить</v-btn>
  </v-form>
    </div>
  </v-container>
</template>

<script>
  import header from "../../mixins/header";
  import listMixin from "../../mixins/listMixin";

  export default {
    name: 'DefaultDeduction',
    mixins: [header, listMixin],

    data: function () {
      return {
        objects: {
            "house": 0,
            "travel": 0,
            "phone": 0,
            "food": 0,
            "user": null
          },
        apiPath: "/api/v1/default-deduction/user_last/",
      }
    },
    computed: {
      totalCount: function () {
        var answer = (parseFloat(this.objects.house) || 0)
            + (parseFloat(this.objects.travel) || 0)
            + (parseFloat(this.objects.phone) || 0)
            + (parseFloat(this.objects.food) || 0)
        return answer
      }
    },
    methods: {
      sendDefaultDeductions(e) {
            e.preventDefault();
            let headers = this.getHeaders();
            let data = {
              "house": this.objects.house,
              "travel": this.objects.travel,
              "phone": this.objects.phone,
              "food": this.objects.food,
              "user": this.objects.user
            }
            this.axios.post(`${this.$apiHost}/api/v1/default-deduction/`, data, {
              headers: headers
            }).then((res) =>{
              this.getData();
        }).catch((res) => {
          this.dropSession(res);
        })
      },
    }
  }
</script>

