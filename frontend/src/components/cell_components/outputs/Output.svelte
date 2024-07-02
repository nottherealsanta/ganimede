<script lang="ts">
  export let cell: any;
  export let is_hover: boolean = false;
  let outputs: never[] = cell.outputs.toJSON();

  let height = 0;
  let width = 0;

  // output components
  import ErrorOutput from "./ErrorOutput.svelte";
  import HtmlOutput from "./HTMLOutput.svelte";
  import ImageOutput from "./ImageOutput.svelte";
  import MarkdownOutput from "./MarkdownOutput.svelte";
  import TextOutput from "./TextOutput.svelte";

  // collapsible chevron
  import Collapsible from "../../utility_components/Collapsible.svelte";
  let output_collapsed: boolean = false;
</script>

<div class="relative">
  <div
    class="outputs"
    style=" max-height: 600px; 
        {cell.state == 'queued' ? 'opacity: 0.5' : ''}
        max-width: 100%;
        "
    bind:clientHeight={height}
    bind:clientWidth={width}
    on:mousedown|stopPropagation={() => {}}
    aria-hidden={true}
  >
    <div
      class="w-full h-auto px-4 py-2
          rounded-br float-bottom
          cursor-default
          pointer-events-auto select-text"
      style="display: {output_collapsed ? 'none' : 'block'}"
    >
      {#if outputs}
        {#each outputs as output}
          <!-- {JSON.stringify(output)} -->
          {#if output["text"]}
            <TextOutput {output} />
          {/if}
          {#if output["output_type"] == "error"}
            <ErrorOutput {output} />
          {/if}
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
        {/each}
      {/if}
    </div>
  </div>
  <!-- if collapsed -->
  {#if output_collapsed}
    <button
      class="collapsed-outputs"
      on:click={() => (output_collapsed = false)}
    >
      Outputs hidden
    </button>
  {/if}
  {#if is_hover}
    <Collapsible bind:is_collapsed={output_collapsed} />
  {/if}
</div>

<style>
  .outputs {
    @apply flex flex-col 
    relative
    w-full h-fit
    
    bg-white
    rounded-b-md
    overflow-y-auto;
    overflow-x: visible;
    scrollbar-width: thin;
  }
  .collapsed-outputs {
    @apply flex
    w-full h-10
    px-4
    mx-0.5
    my-0.5
  bg-white
  text-gray-600
    text-sm
    items-center;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 600;
  }
  .collapsed-outputs:hover {
    @apply bg-gray-100;
  }
</style>
