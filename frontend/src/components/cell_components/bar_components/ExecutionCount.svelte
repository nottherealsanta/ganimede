<script lang="ts">
  export let cell: any;

  $: execution_count =
    cell.execution_count === undefined || cell.execution_count === null
      ? "[ ]"
      : cell.execution_count.toString();
</script>

<div
  class="execution-count {cell.state === 'running'
    ? 'text-gray-200'
    : 'text-gray-500'}"
>
  {execution_count}
</div>

<style>
  .execution-count {
    @apply flex absolute
    h-full w-8
    left-1/2
    items-center justify-center
    cursor-default
    bg-transparent
    text-xs;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 500;
    font-style: normal;
    user-select: none;
  }
</style>
