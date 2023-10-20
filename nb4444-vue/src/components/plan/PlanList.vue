<template>
  <v-container>
    <h1 class="text-center">Планы</h1>
    <v-btn
      color="success"
      class="mb-5"
      dark
      :to="{ name: 'PlanCreate'}"
    >
      Создать
    </v-btn>
    <v-data-table
      :headers="headers"
      :items="objects"
      v-model:items-per-page="itemsPerPage"
      class="elevation-1"
    >
      <template v-slot:item.actions="{ item }">
        <div class="actions-btn">
          <v-row>
            <v-btn icon :to="{ name: 'PlanDetail', params: {planId: item.id} }">
                <v-icon
                class="mr-2"
                >
                  mdi-information
                </v-icon>
              </v-btn>
          `  <v-btn icon :to="{ name: 'PlanUpdate', params: {planId: item.id} }">
              <v-icon
              class="mr-2"
              >
                mdi-pencil
              </v-icon>
            </v-btn>
            <Delete
                @onDelete="getData"
                :objId="item.id"
                :deletePath="'/api/v1/plan/'"
                :titleDelete="'плана'"
                :messageDelete="'план'" ></Delete>
            </v-row>
        </div>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import header from "../../mixins/header";
import listMixin from "../../mixins/listMixin";
import PlanCreate from "./PlanCreate";
import PlanUpdate from "./PlanUpdate";
import Delete from "../common_components/Delete";

export default {
  name: "PlanList",
  components: {PlanUpdate, PlanCreate, Delete},
  mixins: [header, listMixin],

  data: function () {
    return {
      loading: false,
      apiPath: "/api/v1/plan/",
      objects: [],
      itemsPerPage: 10,
      headers: [
        {
          title: 'Дата',
          align: 'start',
          sortable: false,
          value: 'created_at',
        },
        {
          title: 'Пользователь',
          align: 'start',
          sortable: false,
          value: 'user.username',
        },
        {
          title: 'Название плана',
          align: 'start',
          sortable: false,
          value: 'name',
        },
        {
          title: '',
          align: 'start',
          value: 'actions',
        },
      ],
    }
  },
}
</script>