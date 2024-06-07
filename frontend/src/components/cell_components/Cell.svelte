<script lang="ts">
  import NewCellToolbar from "./NewCellToolbar.svelte";
  export let cell_id: string;

  import { cell_map } from "../../scripts/test_nb";
  let cell: any = cell_map[cell_id];
</script>

<div class="cell">
  <NewCellToolbar />
</div>

<style>
  .cell {
    @apply flex relative
    w-auto h-[12rem] mx-8 my-8
    bg-gray-50
    border border-gray-200
    rounded-md;
  }
</style>
