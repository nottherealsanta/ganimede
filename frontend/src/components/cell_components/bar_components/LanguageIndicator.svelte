<script lang="ts">
  export let cellType: string;
  export let isHover: boolean;
</script>

{#if isHover}
  <div class="language-indicator">{cellType}</div>
{/if}

<style>
  .language-indicator {
    @apply flex 
    h-7 w-fit px-2
    mx-1
    items-center justify-center
    cursor-default
    bg-transparent
    rounded-md
    text-xs
    text-gray-500;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 500;
    font-style: normal;
  }
  .language-indicator:hover {
    @apply bg-gray-100;
  }
</style>
