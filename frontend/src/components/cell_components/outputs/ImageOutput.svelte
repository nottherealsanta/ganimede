<!-- <script lang="ts">
  export let output;

  var image = new Image();
  let image_base64 = "";
  $: if (typeof output["data"]["image/png"] !== "string") {
    image_base64 = output["data"]["image/png"][0];
  } else {
    image_base64 = output["data"]["image/png"];
  }
  $: image.src = "data:image/png;base64," + image_base64;
</script>

<div
  class="flex w-fit h-fit max-w-3xl hover:bg-gray-100 dark:hover:bg-neutral-700 rounded"
>
  <img src={image.src} alt="output" />
</div> -->
