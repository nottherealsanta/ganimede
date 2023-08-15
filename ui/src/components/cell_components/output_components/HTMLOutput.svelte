<script>
  export let output;
  let html_string;

  $: if (typeof output["data"]["text/html"] === "string") {
    html_string = output["data"]["text/html"];
  } else {
    html_string = " ";
  }
</script>

<div
  class="flex w-fit h-fit my-1 hover:bg-gray-100 dark:hover:bg-neutral-700 rounded"
>
  {@html html_string}
</div>
