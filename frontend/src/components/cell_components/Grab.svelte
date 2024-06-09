<script lang="ts">
  import { GripVertical } from "lucide-svelte";
  export let is_hover: boolean;
</script>

<div class="left-controls" style="opacity: {is_hover ? 1 : 0};">
  <GripVertical size="16" />
</div>

<style>
  .left-controls {
    @apply absolute flex 
  w-5 h-5
  top-0.5 -left-5
  items-center justify-center
  bg-transparent
  rounded-none
  cursor-grab
  text-gray-400;
  }
  .left-controls:hover {
    @apply bg-gray-100;
  }
  .left-controls:active {
    @apply bg-gray-200;
  }
</style>
