<script lang="ts">
  import { GripVertical } from "lucide-svelte";
  export let is_hover: boolean;
</script>

<div class="left-controls" style="opacity: {is_hover ? 1 : 0};">
  <GripVertical size="20" />
</div>

<style>
  .left-controls {
    @apply absolute flex 
  w-6 h-6 p-1
  top-0 -left-5
  items-center justify-center
  bg-transparent
  rounded-none
  cursor-grab
  text-gray-400;
  }
  .left-controls:hover {
    @apply text-gray-500;
  }
  .left-controls:active {
    @apply text-gray-800;
  }
</style>
