<script lang="ts">
  import CodeCell from "./CodeCell.svelte";
  import Grab from "./Grab.svelte";
  import DeleteCell from "./DeleteCell.svelte";
  import CellBar from "./CellBar.svelte";

  export let cell_id: string;

  import { cell_maps } from "../../scripts/test_nb";
  import {
    active_cell_id,
    is_command_mode,
    cell_stores,
  } from "../../stores/notebook.js";
  import MarkdownCell from "./MarkdownCell.svelte";
  let cell: any = (cell_stores as any)[cell_id];
  let cell_div: HTMLDivElement;

  let is_hover: boolean = false;

  // active cell
  $: is_active = $active_cell_id === cell_id;

  // scroll to active cell
  $: if (is_active && cell_div) {
    cell_div.scrollIntoView({
      behavior: "instant",
      block: "nearest",
    });
  }

  // markdown
  $: is_markdown = cell.type === "markdown";
</script>

<div
  class="cell
  {is_markdown ? 'border-transparent' : 'border-gray-100'}
  {is_hover ? 'ring-1 ring-gray-200' : ''}
  {is_active ? 'ring-2 ring-gray-200 shadow-md shadow-gray-200' : ''}
  "
  role="presentation"
  on:mouseenter={() => {
    is_hover = true;
  }}
  on:mouseleave={() => {
    is_hover = false;
  }}
  bind:this={cell_div}
>
  <!-- Active -->
  {#if is_active}
    <div class="active-cell-indicator"></div>
  {/if}
  <!-- Active & Editable -->
  {#if is_active && !$is_command_mode}
    <div class="active-editable-cell-indicator"></div>
  {/if}

  <!-- Cell Controls -->
  <Grab {is_hover} />
  <DeleteCell {cell_id} {is_hover} />
  <CellBar {cell_id} {is_hover} />

  <!-- Code / Markdown -->
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
    border-2;
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
    w-1 h-full
    rounded-sm
    bg-blue-500;
    pointer-events: none;
  }

  .active-editable-cell-indicator {
    width: calc(100% + 4px);
    height: calc(100% + 4px);
    top: -2px;
    left: -2px;
    @apply absolute
    bg-transparent
    ring-2 ring-blue-500
    rounded-md
    z-20;
    pointer-events: none;
  }
  /* .debug {
    @apply absolute bottom-0 right-0
    bg-gray-200/20
    rounded-md
    text-xs
    text-gray-400
    p-2;
  } */
</style>
