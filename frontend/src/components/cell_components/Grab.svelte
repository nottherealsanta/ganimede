<script lang="ts">
  import { GripVertical } from "lucide-svelte";
  export let is_hover: boolean;
</script>

<div class="left-controls grab-handle" style="opacity: {is_hover ? 1 : 0};">
  <GripVertical size="24" />
</div>

<style>
  .left-controls {
    @apply absolute flex 
  w-8 h-8 p-[7px]
  top-0 -left-7
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
