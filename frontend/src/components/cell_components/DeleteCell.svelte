<script lang="ts">
  import { Trash2 } from "lucide-svelte";
  export let cell_id: string;
  export let is_hover: boolean;
</script>

<button
  class="right-controls"
  style="opacity: {is_hover ? 1 : 0};"
  on:click|stopPropagation={() => {
    console.log("delete cell");
  }}
>
  <Trash2 size="24" />
</button>

<style>
  .right-controls {
    @apply absolute flex 
    w-6 h-6 p-1
    top-[6px] -right-7
    items-center justify-center
    bg-transparent
    rounded-r-md
    text-gray-400
    z-10;
  }
  .right-controls:hover {
    @apply text-gray-600;
  }
  .right-controls:active {
    @apply text-gray-800;
  }
</style>
