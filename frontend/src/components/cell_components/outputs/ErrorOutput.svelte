<script>
  export let output;

  import { AnsiUp } from "ansi_up";
  const ansi_up = new AnsiUp();
  ansi_up.use_classes = true;
</script>

<div class="error select-text py-1 hover:bg-gray-100">
  {#if output["traceback"]}
    {#each output["traceback"] as line}
      <div class="text-pink-700 text-sm whitespace-pre pl-1 pb-0.5">
        {@html ansi_up.ansi_to_html(line)}
      </div>
    {/each}
  {/if}
</div>

<style>
  .error {
    @apply select-text 
    w-fit
    p-1;
    font-family: "IBM Plex Mono", monospace;
  }
  .error:hover {
    @apply bg-gray-100;
  }
</style>
