<script lang="ts">
    import { onMount } from "svelte";
    // import { cells, id_map } from "../../stores/notebook";

    export let cell;
    // outputs
    $: outputs = cell.outputs.toJSON();

    // last heights
    let height = 0;
    let last_height = 0;
    let width = 0;
    let last_width = 0;
    $: if (cell.state == "queued") {
        last_height = height;
        last_width = width;
    } else if (cell.state == "idle") {
        last_height = 0;
        last_width = 0;
    }
    onMount(() => {
        last_height = height;
        last_width = width;
    });

    // output components
    import ErrorOutput from "./output_components/ErrorOutput.svelte";
    import HtmlOutput from "./output_components/HTMLOutput.svelte";
    import ImageOutput from "./output_components/ImageOutput.svelte";
    import MarkdownOutput from "./output_components/MarkdownOutput.svelte";
    import TextOutput from "./output_components/TextOutput.svelte";
</script>

<div
    class="flex bg-nilam dark:bg-nilam-dark rounded-b items-start h-auto w-full justify-center align-stretch overflow-y-auto pointer-events-none"
    style=" max-height: 616px; 
        min-height: {last_height}px; 
        {cell.state == 'queued' ? 'opacity: 0.5' : ''}
        min-width: {last_width}px;
        "
    bind:clientHeight={height}
    bind:clientWidth={width}
    on:mousedown|stopPropagation={() => {}}
>
    <!-- <div class="flex h-full w-6" style="margin-right:7px" /> -->
    <div
        class="w-full h-auto px-1 pl-[6px] py-0.5
                 border-t-2 border-oli-100 dark:border-oli-700 rounded-sm float-bottom mt-0.25 cursor-default pointer-events-auto select-text"
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
