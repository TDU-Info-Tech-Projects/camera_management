import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import ItemList from '@/views/ItemList.vue'
import MyRentItems from '@/views/MyRentItems.vue'
import ProductManage from '@/views/ProductManage.vue'
import UserManage from '@/views/UserManage.vue'
import AdminRentedItems from '@/views/AdminRentedItems.vue'
import {store} from '@/store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'itemList',
    meta: { requireAuth: true, requireAdmin: false },
    component: ItemList,
  },
  {
    path: '/rented',
    name: 'rented',
    meta: { requireAuth: true, requireAdmin: false },
    component: MyRentItems,
  },
  {
    path: '/admin/product',
    name: 'productManage',
    meta: { requireAuth: true, requireAdmin: true },
    component: ProductManage,
  },
  {
    path: '/admin/rented',
    name: 'adminRented',
    meta: { requireAuth: true, requireAdmin: true },
    component: AdminRentedItems,
  },
  {
    path: '/admin/users',
    name: 'adminUserManage',
    meta: { requireAuth: true, requireAdmin: true },
    component: UserManage,
  },
  {
    path: '/login',
    name: 'login',
    meta: { requireAuth: false, requireAdmin: false },
    component: Login,
  },
  {
    path: '/signup',
    name: 'signup',
    meta: { requireAuth: false, requireAdmin: false },
    component: Register,
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach(async (to, from, next) => {
  const isLoginPage = to.matched.some(record => record.path.includes("/login"))
  const isSignupPage = to.matched.some(record => record.path.includes("/signup"))

  const routeToLogin = () => {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  }

  const routeToHome = () => {
    next({ path: '/' })
  }

  if (!store.user) {
    await store.auth()
  }

  const isAuthenticated = !!store.user
  const isAdmin = store.user && store.user.is_admin

  if (isAuthenticated && (isSignupPage || isLoginPage)) {
    routeToHome()
    return
  }

  if (to.matched.some(record => record.meta.requireAuth)) {
    if (!isAuthenticated) {
      routeToLogin()
      return
    }
  }

  if (to.matched.some(record => record.meta.requireAdmin)) {
    if (!isAdmin) {
      routeToHome()
      return
    }
  }

  next()
})

export default router
