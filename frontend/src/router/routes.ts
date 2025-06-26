import type { RouteRecordRaw } from 'vue-router'

export const staticRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/index.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/pages/dashboard/index.vue')
  },
  {
    path: '/auth/login',
    name: 'Login',
    component: () => import('@/pages/auth/login.vue')
  },
  {
    path: '/auth/register',
    name: 'Register',
    component: () => import('@/pages/auth/register.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/pages/index.vue')
  }
]
