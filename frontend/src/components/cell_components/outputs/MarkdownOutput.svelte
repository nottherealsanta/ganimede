<script lang="ts">
  export let output;
  import { marked } from "marked";

  marked.setOptions({
    gfm: true,
    breaks: true,
  });

  $: text = output["data"]["text/markdown"].join("\n");
</script>

<div class="w-fit h-fit p-1 hover:bg-gray-100 rounded">
  {@html marked(text)}
</div>
