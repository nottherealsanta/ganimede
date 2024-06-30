<script lang="ts">
  export let output;
  import { marked } from "marked";
</script>

<div
  class="flex w-fit h-fit hover:bg-gray-100 dark:hover:bg-neutral-700 rounded"
>
  {@html marked(output["data"]["text/markdown"].join(""))}
</div>
