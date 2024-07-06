<script lang="ts">
  import SortableList from "./SortableList.svelte";
  import Cell from "../cell_components/Cell.svelte";
  import NewCellToolbar from "../cell_components/NewCellToolbar.svelte";
  import { drag_move_cells } from "../../stores/notebook";
  import { onMount } from "svelte";

  // @ts-ignore
  function onDragStart(event) {}

  // @ts-ignore
  function onDragEnd(event) {
    drag_move_cells(event);
  }

  // onMount set active cell to the first cell
  import { active_cell_id, cell_ids } from "../../stores/notebook";
  onMount(() => {
    console.log("active cell id set to", $cell_ids[0]);
    active_cell_id.set($cell_ids[0]);
    console.log("$cell_ids", $cell_ids);
  });
</script>

<div
  class="nb"
  on:click={(event) => {
    // if click on nb only
    if (event.target === event.currentTarget) {
      active_cell_id.set("");
    }
  }}
>
  <SortableList
    class="sortable-list flex flex-col w-[85%] min-w-[20rem]"
    group="nested"
    animation={100}
    swapThreshold={0.5}
    onStart={onDragStart}
    onEnd={onDragEnd}
    invertSwap={true}
    touchStartThreshold={100}
    handle=".grab-handle"
    filter=".new-cell-toolbar"
  >
    {#each $cell_ids as cell_id, index (cell_id)}
      <div>
        <Cell {cell_id} {index} />
      </div>
    {/each}
    <!-- final new cell toolbar at the end -->
    <NewCellToolbar index={$cell_ids.length} />
  </SortableList>
</div>

<style>
  .nb {
    @apply flex flex-col
    w-full h-full pt-8 pb-96
    items-center
    bg-transparent;
    overflow-y: overlay;
    min-width: 500px;
    scrollbar-width: thin;
    scrollbar-color: var(--tertiary-color) var(--background-color);
  }
</style>
