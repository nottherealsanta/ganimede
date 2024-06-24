<script lang="ts">
  export let execution_count;
  export let is_markdown: boolean;

  $: exe_count_test =
    execution_count === undefined ? "[ ]" : execution_count.toString();
</script>

{#if !is_markdown}
  <div class="execution-count">{exe_count_test}</div>
{/if}

<style>
  .execution-count {
    @apply flex absolute
    h-full w-8
    left-1/2
    items-center justify-center
    cursor-default
    bg-transparent
    text-xs text-gray-500;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 500;
    font-style: normal;
  }
</style>
