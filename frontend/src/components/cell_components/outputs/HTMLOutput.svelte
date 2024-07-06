<script lang="ts">
  export let output;
  let output_div: HTMLDivElement;
  let html_string: string;
  let html_type: string;
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
  class=" html-output {html_type} {html_type == 'dataframe'
    ? 'dataframe'
    : ''} "
  bind:this={output_div}
>
  {@html html_string}
</div>

<style>
  .html-output {
    @apply w-fit h-fit
    p-1
    bg-transparent 
    border border-transparent
    rounded;
  }
  .html-output:hover {
    @apply border-gray-200;
  }
  .dataframe {
    @apply w-full
    overflow-x-auto;
  }

  :global(.dataframe table) {
    @apply text-sm;
    border-spacing: 0;
    width: fit-content;
    font-family: "Inter", sans-serif;
    font-weight: 400;
  }
  :global(.dataframe thead th) {
    @apply bg-gray-100 py-1 px-2;
    text-align: right;
  }
  :global(.dataframe tbody th) {
    @apply font-normal;
    text-align: right;
  }
  :global(.dataframe tbody tr):nth-child(even) {
    @apply bg-gray-100;
  }
  :global(.dataframe td) {
    @apply py-0 px-2;
    text-align: right;
  }
</style>
