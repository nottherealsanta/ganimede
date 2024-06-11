<script lang="ts">
  import { Play, Sparkles, EllipsisVertical, Trash2 } from "lucide-svelte";

  export let cell_id: string;
  export let is_hover: boolean = false;
</script>

<div class="cell-sidebar">
  <div class="run-button">
    <Play size="16" />
  </div>
  {#if is_hover}
    <div class="cell-status-time">0.0s</div>
    <div class="execution-count">4</div>
    <div class="flex-grow"></div>
    <div class="language-indicator">Python</div>
    <div class="toolbar-button">
      <Sparkles size="16" />
    </div>
    <div class="toolbar-button">
      <EllipsisVertical size="16" />
    </div>
  {/if}
</div>

<style>
  .cell-sidebar {
    @apply flex 
    w-full h-8
    px-1 py-0.5
    items-center
    bg-transparent
    rounded-t;
  }
  .run-button {
    @apply flex 
    h-full w-8
    items-center justify-center
    bg-transparent
    rounded
    cursor-pointer
    text-gray-400;
  }
  .run-button:hover {
    @apply bg-gray-100;
  }
  .run-button:active {
    @apply bg-gray-100 text-gray-800;
  }
  .language-indicator {
    @apply flex 
    h-full w-fit px-1
    mr-2
    items-center justify-center
    cursor-default
    bg-gray-50
    rounded-md
    text-xs
    text-gray-400;
    font-family: "Inter", sans-serif;
    font-weight: 500;
    font-style: normal;
  }
  .cell-status-time {
    @apply flex 
    h-full w-16
    items-center justify-center
    cursor-default
    bg-transparent
    text-xs
    text-gray-400;
    font-family: "Inter", sans-serif;
    font-weight: 500;
    font-style: normal;
  }
  .execution-count {
    @apply flex 
    h-full w-8
    items-center justify-center
    cursor-default
    bg-transparent
    text-xs text-gray-400;
    font-family: "Inter", sans-serif;
    font-weight: 500;
    font-style: normal;
  }
  .toolbar-button {
    @apply relative flex 
    h-full w-8 p-1 
    items-center justify-center
    bg-transparent
    rounded
    text-gray-400;
  }
  .toolbar-button:hover {
    @apply bg-gray-100;
  }
  .toolbar-button:active {
    @apply text-gray-800;
  }
</style>
