<script lang="ts">
  import { active_cell_id } from "../../stores/notebook";

  export let cell_id: string;
  export let is_hover: boolean;
</script>

<div
  class="left-controls grab-handle"
  style="opacity: {is_hover ? 1 : 0};"
  on:click={(e) => {
    active_cell_id.set(cell_id);
  }}
></div>

<style>
  .left-controls {
    @apply absolute flex 
  w-6 p-[7px]
  -top-2 -left-7
  items-center justify-center
  bg-transparent
  rounded-lg
  cursor-grab
  text-gray-400;
    height: calc(100% + 1rem);
  }
  .left-controls:hover {
    @apply bg-gray-50;
  }
</style>
