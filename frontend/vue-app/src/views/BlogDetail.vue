<template>
  <div class="main-content">
    <Header />
    <div v-if="blog" class="blog-detail">
      <h1>{{ blog.title }}</h1>
      <div>作者ID：{{ blog.author_id }}</div>
      <div v-if="blog.cover_image">
        <img :src="blog.cover_image" style="max-width: 400px;" />
      </div>
      <div>{{ blog.content }}</div>
    </div>
    <button class="btn-primary" @click="goHome">返回首页</button>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getBlog } from '../api/blogs';
import Header from '../components/Header.vue';

const route = useRoute();
const router = useRouter();
const blog = ref();

function goHome() { router.push('/'); }

onMounted(async () => {
  const { id } = route.params;
  if (id) {
    const res = await getBlog(Number(id));
    blog.value = res.data;
  }
});
</script>