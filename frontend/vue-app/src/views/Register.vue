<template>
  <div class="auth-container">
    <h2>注册</h2>
    <form @submit.prevent="handleRegister" class="auth-form">
      <input v-model="username" placeholder="用户名" required />
      <input v-model="email" type="email" placeholder="邮箱" required />
      <input v-model="phone" type="text" placeholder="手机号" required />
      <input v-model="password" type="password" placeholder="密码" required />
      <button type="submit">注册</button>
    </form>
    <router-link to="/login">已注册？去登录</router-link>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { register } from '../api/auth';

const router = useRouter();
const username = ref('');
const email = ref('');
const phone = ref('');
const password = ref('');

async function handleRegister() {
  try {
    await register({ username: username.value, email: email.value, phone: phone.value, password: password.value });
    alert('注册成功');
    router.push('/login');
  } catch (e: any) {
    alert(e.response?.data?.detail ?? '注册失败');
  }
}
</script>
<style scoped>
/* 同登录样式略 */
</style>