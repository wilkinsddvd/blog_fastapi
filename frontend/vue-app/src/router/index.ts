import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  { path: '/', component: Home },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})
export default router

// import { createRouter, createWebHistory } from 'vue-router'
// import Home from '../views/Home.vue'
// import Login from '../views/Login.vue'
// import Register from '../views/Register.vue'
// import PasswordReset from '../views/PasswordReset.vue'
// import BlogDetail from '../views/BlogDetail.vue'
// import BlogEditor from '../views/BlogEditor.vue'
// import Profile from '../views/Profile.vue'
//
// const routes = [
//   { path: '/', name: 'Home', component: Home },
//   { path: '/login', name: 'Login', component: Login },
//   { path: '/register', name: 'Register', component: Register },
//   { path: '/password-reset', name: 'PasswordReset', component: PasswordReset },
//   { path: '/blogs/:id', name: 'BlogDetail', component: BlogDetail },
//   { path: '/editor', name: 'BlogEditor', component: BlogEditor },
//   { path: '/profile', name: 'Profile', component: Profile },
// ]
//
// const router = createRouter({
//   history: createWebHistory(),
//   routes,
// })
//
// export default router