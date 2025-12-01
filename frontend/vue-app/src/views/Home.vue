<template>
  <div>
    <h2>首页</h2>
    <router-link to="/login">[登录]</router-link>
  </div>
</template>
<script setup lang="ts"></script>
<!--<template>-->
<!--  <div class="main-content">-->
<!--    <Header />-->
<!--    <div class="blog-list">-->
<!--      <button class="btn-primary" @click="toEditor">发表博客</button>-->
<!--      <BlogCard-->
<!--        v-for="blog in blogs"-->
<!--        :key="blog.id"-->
<!--        :blog="blog"-->
<!--        @click="viewDetail(blog.id)"-->
<!--      />-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->
<!--<script setup lang="ts">-->
<!--import { onMounted, ref } from 'vue';-->
<!--import { useRouter } from 'vue-router';-->
<!--import { listBlogs } from '../api/blogs';-->
<!--import Header from '../components/Header.vue';-->
<!--import BlogCard from '../components/BlogCard.vue';-->

<!--const router = useRouter();-->
<!--const blogs = ref([]);-->

<!--function toEditor() {-->
<!--  router.push('/editor');-->
<!--}-->

<!--function viewDetail(id: number) {-->
<!--  router.push(`/blogs/${id}`);-->
<!--}-->

<!--onMounted(async () => {-->
<!--  const res = await listBlogs();-->
<!--  blogs.value = res.data;-->
<!--});-->
<!--</script>-->
<!--<style>-->
<!--.main-content { padding: 20px; }-->
<!--.blog-list { display: flex; flex-direction: column; gap: 16px; }-->
<!--</style>-->