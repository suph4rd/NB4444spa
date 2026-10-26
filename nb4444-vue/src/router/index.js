import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'


const routes = [
  {
    path: '/',
    name: 'Main',
    meta: { requiresAuth: true },
    component: () => import('../components/Main.vue')
  },

  // Auth
  {
    path: '/login',
    name: 'Login',
    meta: { requiresAuth: false },
    component: () => import('../components/Login.vue')
  },
  {
    path: '/registration',
    name: 'Registration',
    meta: { requiresAuth: false },
    component: () => import('../components/registration/UserCreate.vue')
  },


  // DefaultDeduction
  {
    path: '/default-deduction',
    name: 'DefaultDeduction',
    meta: { requiresAuth: true },
    component: () => import('../components/delault_deduction/DefaultDeduction.vue')
  },

  // Note
  {
    path: '/note',
    name: 'Note',
    meta: { requiresAuth: true },
    component: () => import('../components/note/Note.vue')
  },
  {
    path: '/note/:noteId',
    name: 'NoteUpdate',
    meta: { requiresAuth: true },
    component: () => import('../components/note/NoteUpdate.vue')
  },

    // Plan
  {
    path: '/plan-list',
    name: 'PlanList',
    meta: { requiresAuth: true },
    component: () => import('../components/plan/PlanList.vue')
  },
  {
    path: '/plan/create',
    name: 'PlanCreate',
    meta: { requiresAuth: true },
    component: () => import('../components/plan/PlanCreate.vue')
  },
  {
    path: '/plan/:planId',
    name: 'PlanDetail',
    meta: { requiresAuth: true },
    component: () => import('../components/plan/PlanDetail.vue')
  },
  {
    path: '/plan/:planId/update',
    name: 'PlanUpdate',
    meta: { requiresAuth: true },
    component: () => import('../components/plan/PlanUpdate.vue')
  },
    // Task
    {
    path: '/plan/:planId/task/create',
    name: 'TaskCreate',
    meta: { requiresAuth: true },
    component: () => import('../components/task/TaskCreate.vue')
  },
  {
    path: '/plan/:planId/task/:taskId/update',
    name: 'TaskUpdate',
    meta: { requiresAuth: true },
    component: () => import('../components/task/TaskUpdate.vue')
  },

];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router;

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !store.getters.isAuthenticated) {
    return {
      name: 'Login',
      query: { redirect: to.fullPath },
    }
  }

  if (to.name === 'Login' && store.getters.isAuthenticated) {
    return { name: 'Main' }
  }
})
