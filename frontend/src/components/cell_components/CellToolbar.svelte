<script lang="ts">
  import { Trash2, MessageSquare, Ellipsis, Sparkles } from "lucide-svelte";
  export let is_hover: boolean;
</script>

<div class="cell-toolbar" style="opacity: {is_hover ? 1 : 0};">
  <div class="toolbar-button">
    <Trash2 size="16" />
  </div>
  <div class="toolbar-button">
    <Sparkles size="16" />
  </div>
  <div class="toolbar-button">
    <MessageSquare size="16" />
  </div>
  <div class="toolbar-button">
    <Ellipsis size="16" />
  </div>
</div>

<style>
  .cell-toolbar {
    @apply absolute flex 
    w-fit h-fit px-1 py-0.5
    -top-3 right-0
    items-center justify-center
    bg-white
    rounded-lg
    border border-gray-200;
  }
  .toolbar-button {
    @apply relative flex 
    h-6 w-6 p-1
    items-center justify-center
    bg-transparent
    rounded
    text-sm text-gray-500;
  }
  .toolbar-button:hover {
    @apply bg-gray-100;
  }
  .toolbar-button:active {
    @apply text-gray-800;
  }
</style>
