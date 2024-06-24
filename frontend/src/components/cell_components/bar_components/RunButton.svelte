<script lang="ts">
  import { Play } from "lucide-svelte";

  export let cell: any;
  $: exe_count_test =
    cell.execution_count === undefined ? " " : cell.execution_count.toString();
</script>

<div class="run-button group">
  <button>
    <Play
      size="14"
      strokeWidth="2"
      class="fill-none group-hover:fill-current"
    />
  </button>
</div>

<style>
  .run-button {
    @apply flex 
    h-7 w-7
    items-center justify-center
    bg-transparent
    rounded
    border border-transparent
    cursor-pointer
    text-gray-500;
  }
  .run-button:hover {
    @apply bg-gray-100 text-gray-400;
  }
  .run-button:active {
    @apply bg-gray-200 text-gray-600;
  }
</style>
