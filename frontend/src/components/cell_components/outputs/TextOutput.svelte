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
  class="w-fit max-w-3xl h-auto bg-transparent hover:bg-gray-100 dark:hover:bg-gray-800 my-1 p-1 rounded whitespace-pre-line overflow-hidden text-sm select-text dark:text-white"
  style="font-family: 'IBM Plex Mono', monospace; font-weight: 400;"
>
  {@html display_text}
</div>
