<script setup lang="ts">
const { data } = await useFetch("/api/examples");
const items: Array<{ id: number; name: string }> = data.value?.data ?? [];
</script>

<template>
  <ul>
    <li v-for="item in items" :key="item.id">{{ item.id }}: {{ item.name }}</li>
  </ul>
  <p v-if="items.length === 0">No examples yet.</p>
</template>
