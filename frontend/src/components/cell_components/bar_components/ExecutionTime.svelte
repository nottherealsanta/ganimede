<script lang="ts">
  export let is_markdown: boolean;
</script>

{#if !is_markdown}
  <div class="cell-status-time">0s</div>
{/if}

<style>
  .cell-status-time {
    @apply flex 
    h-full w-16
    items-center justify-center
    cursor-default
    bg-transparent
    text-xs
    text-gray-500;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 500;
    font-style: normal;
  }
</style>
