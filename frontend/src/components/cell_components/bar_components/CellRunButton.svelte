<script lang="ts">
  import { Play } from "lucide-svelte";

  export let cell: any;
  export let is_hover: boolean = false;

  $: exe_count_test =
    cell.execution_count === undefined ? " " : cell.execution_count.toString();
</script>

<div class="run-button">
  {#if is_hover}
    <button>
      <Play size="16" strokeWidth="2" />
    </button>
  {:else}
    <div class="execution-count">{exe_count_test}</div>
  {/if}
</div>

<style>
  .run-button {
    @apply flex 
    h-7 w-7
    items-center justify-center
    bg-transparent
    rounded-md
    border-2 border-gray-50
    cursor-pointer
    text-gray-400;
  }
  .run-button:hover {
    @apply bg-gray-100;
  }
  .run-button:active {
    @apply bg-gray-100 text-gray-700;
  }
  .execution-count {
    @apply text-xs;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 700;
  }
</style>
