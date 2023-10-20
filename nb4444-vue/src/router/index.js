import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'Main',
    component: () => import(/* webpackChunkName: "about" */ '../components/Main.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "about" */ '../components/Login.vue')
  },
  {
    path: '/default-deduction',
    name: 'DefaultDeduction',
    component: () => import(/* webpackChunkName: "about" */ '../components/delault_deduction/DefaultDeduction.vue')
  },

  // Note
  {
    path: '/note',
    name: 'Note',
    component: () => import(/* webpackChunkName: "about" */ '../components/note/Note')
  },
  {
    path: '/note/:noteId',
    name: 'NoteUpdate',
    component: () => import(/* webpackChunkName: "about" */ '../components/note/NoteUpdate.vue')
  },

    // Plan
  {
    path: '/plan-list',
    name: 'PlanList',
    component: () => import(/* webpackChunkName: "about" */ '../components/plan/PlanList.vue')
  },
  {
    path: '/plan/create',
    name: 'PlanCreate',
    component: () => import(/* webpackChunkName: "about" */ '../components/plan/PlanCreate.vue')
  },
  {
    path: '/plan/:planId',
    name: 'PlanDetail',
    component: () => import(/* webpackChunkName: "about" */ '../components/plan/PlanDetail.vue')
  },
  {
    path: '/plan/:planId/update',
    name: 'PlanUpdate',
    component: () => import(/* webpackChunkName: "about" */ '../components/plan/PlanUpdate.vue')
  },
    // Task
    {
    path: '/plan/:planId/task/create',
    name: 'TaskCreate',
    component: () => import(/* webpackChunkName: "about" */ '../components/task/TaskCreate.vue')
  },
  {
    path: '/plan/:planId/task/:taskId/update',
    name: 'TaskUpdate',
    component: () => import(/* webpackChunkName: "about" */ '../components/task/TaskUpdate.vue')
  },

];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router;

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = sessionStorage.getItem('user');

  if (authRequired && !loggedIn) {
    return next('/login');
  }
  next();
});
