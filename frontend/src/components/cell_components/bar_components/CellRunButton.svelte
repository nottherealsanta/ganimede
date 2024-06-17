<script lang="ts">
  import { Play } from "lucide-svelte";

  export let cell: any;
  $: exe_count_test =
    cell.execution_count === undefined ? " " : cell.execution_count.toString();
</script>

<div class="run-button">
  <button>
    <Play size="16" strokeWidth="2" />
  </button>
</div>

<style>
  .run-button {
    @apply flex 
    h-7 w-7
    items-center justify-center
    bg-transparent
    rounded-md
    cursor-pointer
    text-gray-400;
  }
  .run-button:hover {
    @apply bg-gray-200;
  }
  .run-button:active {
    @apply bg-gray-300 text-gray-700;
  }
</style>
