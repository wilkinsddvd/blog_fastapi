import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import PasswordReset from '../views/PasswordReset.vue';
import Profile from '../views/Profile.vue';
import BlogEditor from '../views/BlogEditor.vue';
import BlogDetail from '../views/BlogDetail.vue';
import Messages from '../views/Messages.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/password-reset', component: PasswordReset },
  { path: '/profile', component: Profile },
  { path: '/editor', component: BlogEditor },
  { path: '/blogs/:id', component: BlogDetail, props: true },
  { path: '/messages', component: Messages },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});