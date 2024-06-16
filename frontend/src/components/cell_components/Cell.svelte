<script lang="ts">
  import CodeCell from "./CodeCell.svelte";
  import Grab from "./Grab.svelte";

  export let cell_id: string;

  import { cell_maps } from "../../scripts/test_nb";
  import MarkdownCell from "./MarkdownCell.svelte";
  let cell: any = cell_maps[cell_id];

  let is_hover: boolean = false;

  // active cell
  import { activeCellId } from "../../stores/notebook";
  $: is_active = $activeCellId === cell_id;
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
  on:click={() => {
    activeCellId.set(cell_id);
  }}
>
  <Grab {is_hover} />

  {#if is_active}
    <div class="active-cell-indicator"></div>
  {/if}
  <!-- code / markdown -->
  {#if cell.type === "python" || cell.type === "sql"}
    <CodeCell {cell_id} {is_hover} />
  {:else if cell.type === "markdown"}
    <MarkdownCell {cell_id} />
  {/if}

  <!-- debug -->
  <!-- <div class="debug">
    <p>{cell_id}</p>
    <p>{cell.type}</p>
  </div> -->
  <!----------->
</div>

<style>
  .cell {
    @apply flex flex-col relative
    w-auto h-auto mb-1
    bg-white
    rounded-md
    border-2 border-transparent;
  }

  .active-cell-indicator {
    width: calc(100% + 4px);
    height: calc(100% + 4px);
    top: -2px;
    left: -2px;
    @apply absolute
    bg-transparent
    ring-2 ring-sky-500
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
