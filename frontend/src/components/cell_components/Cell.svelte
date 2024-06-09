<script lang="ts">
  import CodeCell from "./CodeCell.svelte";
  import NewCellToolbar from "./NewCellToolbar.svelte";
  import CellToolbar from "./CellToolbar.svelte";
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
  <!-- code / markdown -->
  {#if cell.type === "code"}
    <CodeCell {cell_id} />
  {:else if cell.type === "markdown"}
    <div class="markdown bg-gray-50 w-full h-full">
      <p>{cell.source}</p>
    </div>
  {/if}
  <NewCellToolbar />
  <Grab {is_hover} />
  <CellToolbar {is_hover} />
  <!-- debug -->
  <!-- <div class="debug">
    <p>{cell_id}</p>
    <p>{cell.type}</p>
  </div> -->
  <!----------->
</div>

<style>
  .cell {
    @apply flex relative
    w-auto h-auto mx-8 mb-5
    max-w-[100rem]
    bg-white
    rounded-md;
  }
  .debug {
    @apply absolute bottom-0 right-0
    bg-gray-200/50
    rounded-md
    text-xs
    p-2;
  }
</style>
