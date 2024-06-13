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
  class="w-fit max-w-3xl h-auto bg-transparent hover:bg-oli-100 dark:hover:bg-oli-800 my-1 pl-1 pr-1 pt-0.5 pb-0.5 rounded whitespace-pre-line overflow-hidden text-xs select-text dark:text-white"
  style="font-family: Roboto Mono; font-size: 0.8rem;"
>
  {@html display_text}
</div>
