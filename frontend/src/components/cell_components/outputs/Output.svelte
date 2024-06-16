<script lang="ts">
  import { onMount } from "svelte";

  export let cell: any;

  let outputs: never[] = cell.outputs;
  // cell.ycell.observeDeep(() => {
  //   // TODO: this is a hack to get the outputs to update, fix this
  //   outputs = cell.outputs.toJSON();
  // });

  // last heights
  let height = 0;
  // let last_height = 0;
  let width = 0;
  // let last_width = 0;
  // $: if (cell.state == "queued") {
  //   last_height = height;
  //   last_width = width;
  // } else if (cell.state == "idle") {
  //   last_height = 0;
  //   last_width = 0;
  // }
  // onMount(() => {
  //   last_height = height;
  //   last_width = width;
  // });

  // output components
  import ErrorOutput from "./ErrorOutput.svelte";
  import HtmlOutput from "./HTMLOutput.svelte";
  import ImageOutput from "./ImageOutput.svelte";
  import MarkdownOutput from "./MarkdownOutput.svelte";
  import TextOutput from "./TextOutput.svelte";

  // toggle collapsed
  // function toggle_output_collapsed(e) {
  //   if (cell.collapsed == "i") {
  //     cell.collapsed = "b";
  //   } else if (cell.collapsed == "b") {
  //     cell.collapsed = "i";
  //   } else if (cell.collapsed == "o") {
  //     cell.collapsed = null;
  //   } else {
  //     cell.collapsed = "o";
  //   }
  // }
  // $: output_collapsed = cell.collapsed == "o" || cell.collapsed == "b";
  let output_collapsed = false;
</script>

<!-- min-height: {last_height}px;  -->
<!-- min-width: {last_width}px; -->
<div
  class="flex rounded-b-md border-t-2 border-gray-100 px-2 items-start h-auto w-full justify-center align-stretch overflow-y-auto pointer-events-none"
  style=" max-height: 616px; 
        {cell.state == 'queued' ? 'opacity: 0.5' : ''}
        max-width: 100%;
        "
  bind:clientHeight={height}
  bind:clientWidth={width}
  on:mousedown|stopPropagation={() => {}}
  aria-hidden={true}
>
  <div
    class="w-full h-auto p-0
                 rounded-br float-bottom cursor-default pointer-events-auto select-text"
  >
    {#if outputs}
      {#each outputs as output}
        {#if output["data"]}
          {#if "text/html" in output["data"]}
            <HtmlOutput {output} />
          {:else if "text/markdown" in output["data"]}
            <MarkdownOutput {output} />
          {:else if "image/png" in output["data"]}
            <ImageOutput {output} />
          {:else if "text/plain" in output["data"]}
            <TextOutput {output} />
          {/if}
        {/if}
        {#if output["text"]}
          <TextOutput {output} />
        {/if}
        {#if output["output_type"] == "error"}
          <ErrorOutput {output} />
        {/if}
      {/each}
    {/if}
  </div>
</div>

<style>
</style>
