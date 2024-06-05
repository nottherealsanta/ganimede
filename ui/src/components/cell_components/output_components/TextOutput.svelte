<script>
  export let output;
  let display_text;
  $: if (output["data"]) {
    if (output["data"]["text/plain"]) {
      display_text = output["data"]["text/plain"];
    }
  } else {
    display_text = output["text"];
  }
</script>

<div
  class="w-fit max-w-3xl h-auto bg-transparent hover:bg-gray-100 dark:hover:bg-zinc-700 my-1 pl-1 pr-1 pt-0.5 pb-0.5 rounded whitespace-pre-line overflow-hidden text-xs select-text dark:text-white"
  style="font-family: Roboto Mono;"
>
  {display_text}
</div>
