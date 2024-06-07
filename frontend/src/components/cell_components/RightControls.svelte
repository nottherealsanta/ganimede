<script lang="ts">
  import { MessageSquare } from "lucide-svelte";
  export let is_hover: boolean;
</script>

<div class="right-controls" style="opacity: {is_hover ? 1 : 0};">
  <MessageSquare size="16" />
</div>

<style>
  .right-controls {
    @apply absolute flex 
  w-5 h-5
  top-0 -right-5
  items-center justify-center
  bg-transparent
  rounded-none
  cursor-grab
  text-gray-400;
  }
  .right-controls:hover {
    @apply bg-gray-100;
  }
  .right-controls:active {
    @apply bg-gray-200;
  }
</style>
