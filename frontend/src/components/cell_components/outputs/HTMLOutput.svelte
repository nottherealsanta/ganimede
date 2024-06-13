<!-- <script>
  export let output;
  let output_div;
  let html_string;
  let html_type;
  $: if (typeof output["data"]["text/html"].join("") === "string") {
    html_string = output["data"]["text/html"].join("");
    // if html_string contains table tag, then set html_type to table
    if (html_string.includes("<table")) {
      html_type = "dataframe";
    }
  } else {
    html_string = "";
    html_type = "";
  }
</script>

<div
  class="flex h-fit my-1 hover:bg-gray-100 dark:hover:bg-neutral-700 rounded {html_type} {html_type ==
  'dataframe'
    ? 'w-fit'
    : 'w-full'} "
  bind:this={output_div}
>
  {@html html_string}
</div> -->
