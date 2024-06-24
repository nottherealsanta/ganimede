<script lang="ts">
  import { Sparkles } from "lucide-svelte";

  export let is_ai_bar_open: boolean;
</script>

<button
  class="toolbar-button {is_ai_bar_open ? 'text-fuchsia-500' : ''}"
  on:click={() => (is_ai_bar_open = !is_ai_bar_open)}
>
  <Sparkles size="16" />
</button>

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
