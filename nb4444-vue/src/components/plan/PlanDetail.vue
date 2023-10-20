<template>
  <div>
    <v-container v-if="objects">
      <h1 class="text-center">План {{objects.name}} ({{objects.user.username}})</h1>

      <v-btn
          color="success"
          dark
          :to="{ name: 'TaskCreate', params: {planId: this.$route.params.planId} }"
        >
          Создать
        </v-btn>
      <v-btn
          color="lighten-2"
          dark
          :to="{ name: 'PlanList'}"
          class="ml-5"
        >
          Назад
        </v-btn>

      <v-data-table
        :headers="headers"
        :items="objects.task_set"
        :items-per-page="10"
        :loading="loading"
      >
        <template v-slot:item.is_ready="{ item }">
          <v-checkbox
            v-model="item.is_ready"
            disabled
          ></v-checkbox>
        </template>

        <template v-slot:item.actions="{ item }">
          <div class="actions-btn">
            <v-btn icon :to="{ name: 'TaskUpdate', params: {taskId: item.id, planId: this.$route.params.planId} }" >
              <v-icon
                class="mr-2"
              >
                mdi-pencil
              </v-icon>
            </v-btn>

            <Delete
                @onDelete="getData"
                :objId="item.id"
                :deletePath="'/api/v1/task/'"
                :titleDelete="'задачи'"
                :messageDelete="'задачу'" >

            </Delete>

          </div>
        </template>
      </v-data-table>
    </v-container>
  </div>
</template>

<script>
import header from "../../mixins/header";
import listMixin from "../../mixins/listMixin";
import TaskCreate from "../task/TaskCreate";
import TaskUpdate from "../task/TaskUpdate";
import Delete from "../common_components/Delete";

export default {
  name: "PlanDetail",
  components: {TaskUpdate, TaskCreate, Delete},
  mixins: [header, listMixin],

  data: function () {
    return {
      loading: false,
      plan: null,
      apiPath: `/api/v1/plan/${this.$route.params.planId}`,
      objects: null,
      headers: [
        {
          title: 'Готово',
          align: 'start',
          sortable: false,
          value: 'is_ready',
        },
        {
          title: 'Дата',
          align: 'start',
          sortable: false,
          value: 'created_at',
        },
        {
          title: 'Раздел',
          align: 'start',
          sortable: false,
          value: 'section.name',
        },
        {
          title: 'Описание',
          align: 'start',
          sortable: false,
          value: 'description',
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

<style>
  .actions-btn {
    display: flex;
    justify-content: end;
  }
</style>