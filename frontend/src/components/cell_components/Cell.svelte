<script lang="ts">
  import CodeCell from "./CodeCell.svelte";
  import Grab from "./Grab.svelte";
  import DeleteCell from "./DeleteCell.svelte";

  export let cell_id: string;

  import { cell_maps } from "../../scripts/test_nb";
  import MarkdownCell from "./MarkdownCell.svelte";
  let cell: any = cell_maps[cell_id];
  let cell_div: HTMLDivElement;

  let is_hover: boolean = false;

  // active cell
  import { active_cell_id, is_command_mode } from "../../stores/notebook";
  $: is_active = $active_cell_id === cell_id;
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
  bind:this={cell_div}
  on:click={(e) => {
    active_cell_id.set(cell_id);
  }}
>
  {#if is_active}
    <div class="active-cell-indicator"></div>
  {/if}
  <Grab {is_hover} />
  <DeleteCell {cell_id} {is_hover} />

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
  .cell::before {
    /* for hover effect to work on grab */
    content: "";
    @apply absolute
    top-0 -left-8
    w-8 h-full
    bg-transparent;
  }
  .cell::after {
    /* for hover effect to work on delete */
    content: "";
    @apply absolute
    top-0 -right-8
    w-8 h-full
    bg-transparent;
  }
  .active-cell-indicator {
    width: calc(100% + 35px);
    height: calc(100%);
    top: 0px;
    left: -30px;
    @apply absolute
    bg-sky-400/10
    border-r-2 border-sky-600
    z-0;
    pointer-events: none;
  }
  .active-cell-indicator::before {
    content: "";
    @apply absolute
    top-0 left-0
    w-1 h-full
    rounded-sm
    bg-sky-600;
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
