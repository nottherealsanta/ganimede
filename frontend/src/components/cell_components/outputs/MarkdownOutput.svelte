<script lang="ts">
  export let output;
  import { marked } from "marked";
</script>

<div class="w-fit h-fit p-1 hover:bg-gray-100 rounded">
  {@html marked(output["data"]["text/markdown"].join(""))}
</div>
