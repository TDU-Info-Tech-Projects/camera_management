import Vue from 'vue'
import VueRouter from 'vue-router'
import App from '@/App.vue'
import vuetify from './plugins/vuetify'
// import About from '@/About.vue'


Vue.config.productionTip = false
Vue.use(VueRouter)

const routes = [
  { path: '/',      component: App },
  // { path: '/about', component: About }
]

const router = new VueRouter({
  routes
})


Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')