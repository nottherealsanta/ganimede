<script lang="ts">
  import { Plus } from "lucide-svelte";
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="new-cell-toolbar" on:click|stopPropagation>
  <div class="line" />
  <div class="toolbar-button">Python</div>
  <div class="line" />
  <div class="toolbar-button">SQL</div>
  <div class="line" />
  <div class="toolbar-button">Markdown</div>
</div>

<style>
  .new-cell-toolbar {
    @apply flex absolute
    w-full h-2
    -top-4
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
    @apply absolute h-[1px] w-[98%] bg-gray-200;
  }
  .toolbar-button {
    @apply flex 
    w-fit h-6 px-2 mx-2
    items-center
    bg-white
    rounded-lg
    border border-gray-200
    text-sm
    text-gray-500
    z-10
    shadow-sm;
    font-family: "Inter", sans-serif;
    font-weight: 500;
    user-select: none;
  }
  .toolbar-button:hover {
    @apply bg-gray-50;
  }
  .toolbar-button:active {
    @apply bg-gray-100 
    text-blue-500
    border border-blue-500;
  }
</style>
