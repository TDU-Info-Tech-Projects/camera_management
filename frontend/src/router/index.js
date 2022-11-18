import Vue from 'vue'
import VueRouter from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import UserList from '../views/UserList.vue'
import About from '../views/AboutView.vue'
import ChartsTest from '../views/ChartsTest.vue'
import AdminTop from '../views/AdminTop.vue'
import ListsTest from '../views/ListsTest.vue'



Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'UserList',
    component: UserList,
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: About,
    // component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/admin',
    name: 'admin',
    // component: () => import(/* webpackChunkName: "admin" */ '../views/AdminTop.vue')
    component: AdminTop,
  },
    {
    path: '/charts',
    name: 'charts',
    component: ChartsTest,
    // component: () => import(/* webpackChunkName: "admin" */ '../views/ChartsTest.vue')
  },
  {
    path: '/lists',
    name: 'lists',
    component: ListsTest,
    // component: () => import(/* webpackChunkName: "admin" */ '../views/ChartsTest.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
