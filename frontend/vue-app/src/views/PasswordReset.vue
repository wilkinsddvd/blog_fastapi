<template>
  <div class="auth-container">
    <h2>找回密码</h2>
    <form v-if="!step2" @submit.prevent="handleSendCode">
      <input v-model="phone" placeholder="填写手机号" />
      <button type="submit">发送验证码</button>
    </form>
    <form v-else @submit.prevent="handleReset">
      <input v-model="code" placeholder="验证码" />
      <input v-model="newPassword" type="password" placeholder="新密码" />
      <button type="submit">重置密码</button>
    </form>
    <div v-if="msg">{{ msg }}</div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import { requestPasswordReset, resetPassword } from '../api/auth';

const phone = ref('');
const code = ref('');
const newPassword = ref('');
const msg = ref('');
const step2 = ref(false);

async function handleSendCode() {
  try {
    const res = await requestPasswordReset(phone.value);
    msg.value = '验证码（仅供开发调试）: ' + res.data.otp;
    step2.value = true;
  } catch (e: any) {
    msg.value = e.response?.data?.detail ?? '发送失败';
  }
}
async function handleReset() {
  try {
    await resetPassword(phone.value, code.value, newPassword.value);
    msg.value = '密码已重置，请前往登录';
  } catch (e: any) {
    msg.value = e.response?.data?.detail ?? '重置失败';
  }
}
</script>