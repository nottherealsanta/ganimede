<script lang="ts">
  import CodeCell from "./CodeCell.svelte";
  import NewCellToolbar from "./NewCellToolbar.svelte";
  import Grab from "./Grab.svelte";

  export let cell_id: string;

  import { cell_maps } from "../../scripts/test_nb";
  let cell: any = cell_maps[cell_id];

  let is_hover: boolean = false;
</script>

<div
  class="cell"
  role="presentation"
  on:mouseenter={() => {
    is_hover = true;
  }}
  on:mouseleave={() => {
    is_hover = false;
  }}
>
  <Grab {is_hover} />
  <NewCellToolbar />

  <!-- code / markdown -->
  {#if cell.type === "code"}
    <CodeCell {cell_id} {is_hover} />
  {:else if cell.type === "markdown"}
    <div
      class="markdown bg-transparent p-2 w-full h-full border-l-2 border-gray-200"
    >
      <p>{cell.source}</p>
    </div>
  {/if}

  <!-- debug -->
  <div class="debug">
    <p>{cell_id}</p>
    <p>{cell.type}</p>
  </div>
  <!----------->
</div>

<style>
  .cell {
    @apply flex relative
    w-auto h-auto mb-8 
    bg-white
    rounded-md;
  }
  .debug {
    @apply absolute bottom-0 right-0
    bg-gray-200/20
    rounded-md
    text-xs
    text-gray-400
    p-2;
  }
</style>
