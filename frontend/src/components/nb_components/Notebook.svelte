<script lang="ts">
  import Cell from "../cell_components/Cell.svelte";

  import { cells } from "../../scripts/test_nb";
  $: console.log(cells);
</script>

<div class="nb">
  <div class="cells">
    {#each cells as cell_id}
      <Cell {cell_id} />
    {/each}
  </div>
</div>

<style>
  .nb {
    @apply flex flex-col 
    w-full h-full px-20 pt-8
    bg-transparent;
    margin: 0 auto;
    overflow-y: scroll;
    min-width: 500px;
    scrollbar-width: thin;
    scrollbar-color: var(--tertiary-color) var(--background-color);
  }

  .cells {
    @apply flex flex-col
    w-full;
  }
</style>
