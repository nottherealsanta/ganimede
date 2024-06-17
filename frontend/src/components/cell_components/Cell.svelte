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
  import { activeCellId } from "../../stores/notebook";
  $: is_active = $activeCellId === cell_id;

  // deactivate cell when clicked outside
  function handleClickOutside(event: MouseEvent) {
    if (cell_div && !cell_div.contains(event.target as Node)) {
      activeCellId.set("");
    }
  }

  $: {
    if (is_active) {
      document.addEventListener("click", handleClickOutside);
    } else {
      document.removeEventListener("click", handleClickOutside);
    }
  }
  import { onDestroy } from "svelte";
  import { Delete } from "lucide-svelte";
  onDestroy(() => {
    document.removeEventListener("click", handleClickOutside);
  });
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
    activeCellId.set(cell_id);
  }}
>
  <Grab {is_hover} />
  <DeleteCell {cell_id} {is_hover} />

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
    width: calc(100% + 4px);
    height: calc(100% + 4px);
    top: -2px;
    left: -2px;
    @apply absolute
    bg-transparent
    ring-2 ring-gray-800
    rounded-md;
    pointer-events: none;
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
