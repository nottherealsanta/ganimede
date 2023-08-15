<script lang="ts">
  export let output;

  $: if (output["data"]) {
    if (output["data"]["text/plain"]) {
      output["text"] = output["data"]["text/plain"];
    }
  } else {
    output["text"] = output["text"];
  }
  let display_text;
  $: if (typeof output["text"] === "string") {
    display_text = output["text"];
  } else {
    display_text = " ";
  }
</script>

<div
  class="w-fit max-w-3xl h-auto bg-transparent hover:bg-gray-100 dark:hover:bg-zinc-700 my-1 pl-1 pr-1 pt-0.5 pb-0.5 rounded whitespace-pre-line overflow-hidden text-xs select-text dark:text-white"
  style="font-family: Roboto Mono;"
>
  {display_text}
</div>
