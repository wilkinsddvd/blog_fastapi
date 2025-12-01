<template>
  <div class="auth-container">
    <h2>登录</h2>
    <form @submit.prevent="handleLogin" class="auth-form">
      <input v-model="username" type="text" placeholder="用户名" required />
      <input v-model="password" type="password" placeholder="密码" required />
      <button type="submit">登录</button>
    </form>
    <router-link to="/register">没有账号？注册</router-link>
    <router-link to="/password-reset">忘记密码？</router-link>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login } from '../api/auth';

const router = useRouter();
const username = ref('');
const password = ref('');

async function handleLogin() {
  try {
    const res = await login(username.value, password.value);
    localStorage.setItem('access_token', res.data.access_token);
    router.push('/');
  } catch (e: any) {
    alert(e.response?.data?.detail ?? '登录失败');
  }
}
</script>

<style scoped>
.auth-container { max-width: 360px; margin: 80px auto; padding: 40px; background: #fff; border-radius: 12px; box-shadow: 0 2px 16px #002fa740;}
.auth-form input { width: 100%; margin: 8px 0; padding: 12px; border-radius: 8px; border: 1px solid #002fa7;}
button { width: 100%; background: #002fa7; color: #fff; border: none; border-radius: 8px; padding: 12px; font-size: 18px;}
a { display: block; margin-top: 16px; color: #002fa7; text-align: right;}
</style>