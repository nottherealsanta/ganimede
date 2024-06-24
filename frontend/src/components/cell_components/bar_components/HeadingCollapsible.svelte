<script lang="ts">
  import { ChevronDown } from "lucide-svelte";

  export let is_heading: boolean;
</script>

{#if is_heading}
  <button class="toolbar-button" on:click|stopPropagation>
    <ChevronDown size="16" class="text-gray-500" />
  </button>
{/if}

<style>
  .toolbar-button {
    @apply relative flex 
    h-7 w-7 p-1 
    items-center justify-center
    bg-transparent
    rounded-md
    text-gray-500;
  }
  .toolbar-button:hover {
    @apply bg-gray-100;
  }
  .toolbar-button:active {
    @apply text-gray-800;
  }
</style>
