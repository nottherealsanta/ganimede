<script lang="ts">
  import { Plus } from "lucide-svelte";
  export let index: number;
</script>

<div class="new-cell-toolbar">
  <div class="line" />
  <div class="toolbar-button">
    <Plus class="mr-1" size="16" />Python
  </div>
  <div class="line" />
  <div class="toolbar-button">
    <Plus class="mr-1" size="16" />SQL
  </div>
  <div class="line" />
  <div class="toolbar-button">
    <Plus class="mr-1" size="16" />Markdown
  </div>
</div>

<style>
  .new-cell-toolbar {
    @apply flex relative
    w-full h-2
    items-center justify-center 
    bg-transparent 
    rounded-full;
    cursor: pointer;
    opacity: 0;
  }
  .new-cell-toolbar:hover {
    opacity: 1;
    @apply bg-gray-50;
  }
  .line {
    @apply absolute h-[2px] w-full bg-gray-300;
  }
  .toolbar-button {
    @apply flex 
    w-fit h-6 px-2 mx-2
    items-center
    bg-white
    rounded-lg
    border border-gray-300
    text-sm
    text-gray-500
    z-10;
    font-family: "Inter", sans-serif;
  }
  .toolbar-button:hover {
    @apply bg-gray-100;
  }
  .toolbar-button:active {
    @apply bg-gray-200 text-gray-700;
  }
</style>
