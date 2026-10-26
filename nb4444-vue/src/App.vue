<template>
  <v-app>
    <v-app-bar class="app-bar" color="green-accent-3">
      <v-app-bar-nav-icon v-if="$store.getters.isAuthenticated" @click="onLeftMenu"></v-app-bar-nav-icon>
      <v-app-bar-title class="text-center">БЧ</v-app-bar-title>
      <v-btn
        v-if="$store.getters.isAuthenticated"
        class="mr-2"
        variant="outlined"
        prepend-icon="mdi-logout"
        @click="logout"
      >
        Выход
      </v-btn>
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

    <v-main class="app-main bg-blue-grey-lighten-5">
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer class="app-footer bg-green-accent-4">
      <strong>© 2021 Andrei Biarniak</strong>
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
.app-bar .v-toolbar__content {
  width: 100%;
}

.app-main {
  flex: 1 0 auto;
}

.app-footer {
  display: flex;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 8px 16px;
  text-align: center;
}

.main-content {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}
</style>
