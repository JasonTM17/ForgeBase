<script lang="ts">
  import { appName } from "$lib/config.js";

  import type { PageData } from "./$types";

  let { data }: { data: PageData } = $props();
</script>

<svelte:head>
  <title>{appName}</title>
</svelte:head>

<main>
  <h1>{appName}</h1>
  <section aria-labelledby="examples-heading">
    <h2 id="examples-heading">Examples</h2>
    <ul>
      {#each data.items as item (item.id)}
        <li>{item.id}: {item.name}</li>
      {/each}
    </ul>
    {#if data.items.length === 0}
      <p>No examples yet.</p>
    {/if}
  </section>
</main>
