<template>
  <div class="main-content">
    <Header />
    <form @submit.prevent="submitBlog">
      <input v-model="title" placeholder="博客标题" required />
      <textarea v-model="content" rows="10" placeholder="内容..." required />
      <input type="file" @change="onCoverChange" />
      <button type="submit" class="btn-primary">发表博客</button>
    </form>
    <div v-if="msg">{{ msg }}</div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { createBlog } from '../api/blogs';
import Header from '../components/Header.vue';

const router = useRouter();
const title = ref('');
const content = ref('');
const coverFile = ref<File | null>(null);
const msg = ref('');

function onCoverChange(e: Event) {
  const files = (e.target as HTMLInputElement).files;
  if (files && files.length > 0) {
    coverFile.value = files[0];
  }
}

async function submitBlog() {
  try {
    const formData = new FormData();
    formData.append('title', title.value);
    formData.append('content', content.value);
    if (coverFile.value) formData.append('cover', coverFile.value);
    await createBlog(formData);
    msg.value = '发表成功';
    setTimeout(() => router.push('/'), 1200);
  } catch (e: any) {
    msg.value = e.response?.data?.detail ?? '发表失败';
  }
}
</script>