import { createRouter, createWebHashHistory } from 'vue-router'
import login from '../views/auth/login.vue'
import register from '../views/auth/register.vue'
import dashboard from '../views/dashboard/dashboard.vue'
import cart from '../views/cart/cart.vue'
import store_manager_dashboard from '../views/manager_dash/manager_dashboard.vue'
import admin_dashboard from '../views/admin_dash/admin_dashboard.vue' 
import forbidden from '../views/error pages/forbidden.vue'
import products from '../views/manager_dash/manager_products.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: login
  },
  {
    path: '/register',
    name: 'register',
    component: register
  },
  {
    path: '/:id',
    name: 'Dashboard',
    component: dashboard
  },
  {
    path: '/store_manager_dashboard/:id',
    name: 'store_manager_dashboard',
    component: store_manager_dashboard
  },
  {
    path: '/:category/products/:id',
    name: 'products',
    component: products
  },
  {
    path: '/admin_dashboard/:id',
    name: 'admin_dashboard',
    component: admin_dashboard
  },
  {
    path: '/cart/:id',
    name: 'Cart',
    component: cart
  },
  {
    path: '/forbidden',
    name: 'forbidden',
    component: forbidden
  },

]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
