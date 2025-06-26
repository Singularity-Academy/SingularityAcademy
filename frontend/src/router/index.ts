import { createRouter, createWebHistory } from 'vue-router'
import { staticRoutes } from './routes'

const router = createRouter({
  history: createWebHistory(),
  routes: staticRoutes
})

export default router
