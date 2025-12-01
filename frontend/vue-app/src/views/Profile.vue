<template>
  <div class="main-content">
    <Header />
    <div v-if="user">
      <div>用户名: {{ user.username }}</div>
      <div>邮箱: {{ user.email }}</div>
      <div>手机号: {{ user.phone }}</div>
      <div>bio: {{ user.bio }}</div>
      <div>
        头像: <img :src="user.avatar" v-if="user.avatar" style="width:100px;" />
        <input type="file" @change="uploadAvatar" />
      </div>
      <form @submit.prevent="saveBio">
        <input v-model="bio" placeholder="个人介绍/Bio" />
        <button>保存</button>
      </form>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getProfile, updateProfile, uploadAvatar } from '../api/profile';
import Header from '../components/Header.vue';

const user = ref<any>(null);
const bio = ref('');

onMounted(async () => {
  const res = await getProfile();
  user.value = res.data;
  bio.value = user.value.bio || '';
});

async function saveBio() {
  await updateProfile({ bio: bio.value });
  const res = await getProfile();
  user.value = res.data;
}

async function uploadAvatar(e: Event) {
  const files = (e.target as HTMLInputElement).files;
  if (files && files.length > 0) {
    const form = new FormData();
    form.append('file', files[0]);
    await uploadAvatar(form);
    const res = await getProfile();
    user.value = res.data;
  }
}
</script>