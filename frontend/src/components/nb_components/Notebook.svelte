<script>
  import SortableList from "./SortableList.svelte";
  import Cell from "../cell_components/Cell.svelte";

  import { cells } from "../../scripts/test_nb";
  $: console.log(cells);

  // @ts-ignore
  function onDragStart(event) {}

  // @ts-ignore
  function onDragEnd(_event) {}
</script>

<!-- 
<div class="nb">
  <div class="cells">
    {#each cells as cell_id}
      <Cell {cell_id} />
    {/each}
  </div>
</div> -->
<!-- 
 -->
<div class="nb">
  <SortableList
    class="sortable-list flex flex-col w-[85%] min-w-[80rem]"
    group="nested"
    animation={100}
    swapThreshold={0.5}
    onStart={onDragStart}
    onEnd={onDragEnd}
    invertSwap={true}
    touchStartThreshold={100}
    handle=".grab-handle"
  >
    {#each cells as cell_id, index (cell_id)}
      <Cell {cell_id} />
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
