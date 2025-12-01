<template>
  <header class="header">
    <span @click="goHome" class="logo">Klein Blog</span>
    <router-link to="/">首页</router-link>
    <router-link to="/profile">个人中心</router-link>
    <router-link to="/messages">私信</router-link>
    <router-link to="/login" v-if="!isLogin">登录</router-link>
    <button v-if="isLogin" @click="logout">登出</button>
  </header>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

const isLogin = ref(!!localStorage.getItem('access_token'));
function goHome() { router.push('/'); }
function logout() {
  localStorage.removeItem('access_token');
  isLogin.value = false;
  router.push('/login');
}
</script>
<style scoped>
.header {
  background: #002fa7;
  color: #fff;
  padding: 12px 32px;
  font-size: 20px;
  display: flex;
  gap: 24px;
  align-items: center;
  border-radius: 0 0 16px 16px;
}
.logo { font-weight: bold; cursor: pointer; }
a { color: #fff; font-weight: bold; text-decoration: none; }
button { background: #fff; color: #002fa7; border-radius: 8px; border: none; padding: 4px 16px; margin-left: 8px;}
</style>