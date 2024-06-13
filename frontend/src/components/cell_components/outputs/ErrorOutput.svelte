<!-- <script>
  export let output;

  import { default as AnsiUp } from "ansi_up";
  const ansi_up = new AnsiUp();
  ansi_up.use_classes = true;
</script>

<div class="select-text py-1 hover:bg-gray-100 dark:hover:bg-oli-700">
  {#if output["traceback"]}
    {#each output["traceback"] as line}
      <div
        class="text-gray-800 dark:text-white whitespace-pre font-mono pl-1 pb-0.5"
      >
        {@html ansi_up.ansi_to_html(line)}
      </div>
    {/each}
  {/if}
</div> -->
