<script lang="ts">
  import NewCellToolbar from "./NewCellToolbar.svelte";
  import LeftControls from "./LeftControls.svelte";

  export let cell_id: string;

  import { cell_map } from "../../scripts/test_nb";
  let cell: any = cell_map[cell_id];

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
  <NewCellToolbar />

  <LeftControls {is_hover} />
</div>

<style>
  .cell {
    @apply flex relative
    w-auto h-[12rem] mx-8 mb-5
    bg-gray-200
    
    rounded-md;
  }
</style>
