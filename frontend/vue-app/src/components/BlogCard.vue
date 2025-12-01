<template>
  <div class="card" @click="$emit('click')">
    <div class="card-header">{{ blog.title }}</div>
    <div class="card-meta">作者：{{ blog.author_id }} 时间：{{ blog.created_at }}</div>
    <div class="card-body">{{ blog.content.slice(0, 80) }}{{ blog.content.length > 80 ? '...' : '' }}</div>
  </div>
</template>
<script setup lang="ts">
defineProps<{ blog: any }>();
</script>
<style scoped>
.card { padding: 16px; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #002fa720; cursor:pointer;}
.card-header { font-size: 18px; color: #002fa7; font-weight: bold; }
.card-meta { font-size: 12px; color: #888;}
.card-body { font-size: 15px; margin-top: 8px;}
</style>