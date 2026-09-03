<script lang="ts">
  import { page } from "$app/state";
</script>

<main>
  <h1>Something went wrong</h1>
  <p role="alert">{page.error?.message ?? "An unexpected error occurred."}</p>
</main>
