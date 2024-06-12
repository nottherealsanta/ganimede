<script>
  import SortableList from "./SortableList.svelte";
  import Cell from "../cell_components/Cell.svelte";
  import NewCellToolbar from "../cell_components/NewCellToolbar.svelte";
  import { onMount } from "svelte";
  import { cell_ids } from "../../scripts/test_nb";

  // @ts-ignore
  function onDragStart(event) {}

  // @ts-ignore
  function onDragEnd(event) {}

  // onMount set active cell to the first cell
  import { activeCellId } from "../../stores/notebook";
  onMount(() => {
    activeCellId.set(cell_ids[0]);
  });
</script>

<div class="nb">
  <SortableList
    class="sortable-list flex flex-col w-[85%] min-w-[40rem]"
    group="nested"
    animation={100}
    swapThreshold={0.5}
    onStart={onDragStart}
    onEnd={onDragEnd}
    invertSwap={true}
    touchStartThreshold={100}
    handle=".grab-handle"
  >
    {#each cell_ids as cell_id, index (cell_id)}
      <Cell {cell_id} />
      <NewCellToolbar {index} />
    {/each}
  </SortableList>
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
</style>
