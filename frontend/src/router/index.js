import Vue from 'vue'
import VueRouter from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import UserList from '@/views/UserList.vue'
import AdminTop from '@/views/AdminTop.vue'
import Login from '@/views/Login.vue'
import ItemList from '@/views/ItemList.vue'
import MyRentItems from '@/views/MyRentItems.vue'
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
    path: '/admin',
    name: 'admin',
    meta: { requireAuth: true, requireAdmin: true },
    component: AdminTop,
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
    component: Login,
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
  // TODO: implement
  const isAdmin = false

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
