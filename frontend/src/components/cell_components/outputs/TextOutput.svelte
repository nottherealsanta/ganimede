<script lang="ts">
  export let output;

  let display_text: string = "";

  $: if (output["data"]) {
    if (output["data"]["text/plain"]) {
      display_text = output["data"]["text/plain"]
        .join("")
        .replace(/ /g, "&nbsp;");
    }
  } else {
    display_text = output["text"].join("").replace(/ /g, "&nbsp;");
  }
</script>

<div
  class="text-output"
  style="font-family: 'IBM Plex Mono', monospace; font-weight: 400;"
>
  {@html display_text}
</div>

<style>
  .text-output {
    @apply w-fit min-w-32
    h-auto bg-transparent  
    my-1 p-1 rounded
     whitespace-pre-line 
     overflow-hidden text-sm select-text;
  }
  .text-output:hover {
    @apply bg-gray-100;
  }
</style>
