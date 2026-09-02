<script lang="ts">
  import { appName } from "./config.js";
  import { exampleService } from "./services/exampleService.svelte.js";

  let items = $state(exampleService.list());

  function add(): void {
    const name = globalThis.prompt("Name?");
    if (name && name.trim()) {
      exampleService.create(name);
      items = exampleService.list();
    }
  }
</script>

<main>
  <h1>{appName}</h1>
  {#if error}
    <div role="alert">
      <h2>Something went wrong</h2>
      <pre>{error}</pre>
    </div>
  {:else}
    <section>
      <h2>Examples</h2>
      <button type="button" onclick={add}>Add</button>
      <ul>
        {#each items as item (item.id)}
          <li>{item.id}: {item.name}</li>
        {/each}
      </ul>
    </section>
  {/if}
</main>
