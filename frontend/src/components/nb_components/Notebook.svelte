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
    @apply flex flex-row 
    w-full h-full pt-8 
    justify-center
    min-w-[900px]
    bg-transparent;
    overflow-y: overlay;
    min-width: 500px;
    scrollbar-width: thin;
    scrollbar-color: var(--tertiary-color) var(--background-color);
  }

  .cells {
    @apply flex flex-col
    w-[85%]
    min-w-[80rem];
  }
</style>
