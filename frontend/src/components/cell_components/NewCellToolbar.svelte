<script lang="ts">
  import { X, Sparkles } from "lucide-svelte";
  import AiBar from "./AiBar.svelte";
  export let index;

  let ai_bar: boolean = false;
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="new-cell-toolbar" on:click|stopPropagation>
  <div class="line" />
  <button class="toolbar-button">Python</button>
  <button class="toolbar-button">SQL</button>
  <button class="toolbar-button">Markdown</button>
  <button class="toolbar-button" on:click={() => (ai_bar = !ai_bar)}>
    {#if ai_bar}
      <X size="14" />
    {:else}
      <Sparkles size="14" />
    {/if}
  </button>
</div>

{#if ai_bar}
  <div class="my-2">
    <AiBar bind:ai_bar />
  </div>
{/if}

<style>
  .new-cell-toolbar {
    @apply flex relative
    w-full h-2 mb-1
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
    @apply absolute h-[1px] w-[98%] bg-gray-300;
  }
  .toolbar-button {
    @apply flex 
    w-fit h-6 px-2 mx-2
    items-center
    bg-white
    rounded-md
    border border-gray-200
    text-sm
    text-gray-500
    z-10
    shadow-md;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 500;
    user-select: none;
  }
  .toolbar-button:hover {
    @apply bg-gray-100 border-gray-300 text-gray-600;
  }
  .toolbar-button:active {
    @apply bg-gray-100 
    text-gray-700
    shadow-none;
  }
</style>
