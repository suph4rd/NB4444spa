<template>
  <v-app>

    <v-app-bar color="green-accent-3">
      <v-app-bar-nav-icon v-if="$store.getters.isAuthenticated" @click="onLeftMenu"></v-app-bar-nav-icon>
      <v-col
      class="text-center"
    >
      <h1>БЧ</h1>
    </v-col>
    <v-col v-if="$store.getters.isAuthenticated" cols="2" class="text-end">
      <button @click="logout">Выход</button>
    </v-col>
    </v-app-bar>

    <v-navigation-drawer
        v-if="$store.getters.isAuthenticated"
        v-model="leftMenu"
        location="left"
        temporary
      >
        <v-list>
          <v-list-item
            v-for="item in menuItems"
            :key="item.title"
            :title="item.title"
            :to='{"name": item.link}'
          ></v-list-item>
        </v-list>
      </v-navigation-drawer>

    <!-- Sizes your content based upon application components -->
    <v-main class="bg-blue-grey-lighten-5">

      <!-- Provides the application the proper gutter -->
      <v-container fluid>

        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer class="bg-green-accent-4 pa-0">
    <v-col
      class="text-center"
      cols="12"
    >
      <strong>© 2021 Andrey Bernyak</strong>
    </v-col>
  </v-footer>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: function () {
    return {
      leftMenu: false,
      apiHost: location.origin,
      menuItems: [
        {
          title: 'Главная страница',
          link: 'Main',
        },
        {
          title: 'Стандартные вычеты',
          link: 'DefaultDeduction',
        },
        {
          title: 'Заметки',
          link: 'Note',
        },
        {
          title: 'Планы',
          link: 'PlanList',
        },
      ],
    }
  },
  methods: {
    onLeftMenu(){
      this.leftMenu = !this.leftMenu
    },
    updateBotMessages(){
      this.axios.get(`${this.$apiHost}/api/v1/bot-response/`).then((result) =>{
        if (result.status === 200) {
          alert("Запрос на подгрузку записей успешно получен!")
        } else {
          alert("Ошибка отправки запроса!")
        }
      })
    },
    logout() {
      this.$store.commit('clearUser')
      this.$router.replace({ name: 'Login' })
    }
  }
};
</script>

<style>
.main-content {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
</style>
