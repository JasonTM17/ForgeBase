<script setup lang="ts">
const config = useRuntimeConfig();
const appName = String(config.public.appName ?? "").trim();
if (!appName) {
  throw new Error("Missing required runtime configuration: NUXT_PUBLIC_APP_NAME");
}

const { data } = await useFetch("/api/examples");
const items: Array<{ id: number; name: string }> = data.value?.data ?? [];
</script>

<template>
  <h1>{{ appName }}</h1>
  <ul>
    <li v-for="item in items" :key="item.id">{{ item.id }}: {{ item.name }}</li>
  </ul>
  <p v-if="items.length === 0">No examples yet.</p>
</template>
