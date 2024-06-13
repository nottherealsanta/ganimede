<script lang="ts">
  import { Play } from "lucide-svelte";

  export let cell: any;
  export let is_hover: boolean = false;

  $: exe_count_test =
    cell.execution_count === undefined ? " " : cell.execution_count.toString();
</script>

<div class="prime-button">
  {#if is_hover}
    <button>
      <Play size="16" />
    </button>
  {:else}
    <div class="execution-count">{exe_count_test}</div>
  {/if}
</div>

<style>
  .prime-button {
    @apply flex 
    h-7 w-7
    items-center justify-center
    bg-transparent
    rounded
    cursor-pointer
    text-gray-400;
  }
  .execution-count {
    @apply text-xs;
    font-family: "JetBrains Mono", monospace;
  }
</style>
