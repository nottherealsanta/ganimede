<script lang="ts">
    import { onMount } from "svelte";
    export let cell_id;
    import { cells, id_map } from "../../stores/notebook";

    // outputs
    $: outputs = $cells[$id_map[cell_id]].outputs;

    // last heights
    $: cell = $cells[$id_map[cell_id]];
    let height = 0;
    let last_height = 0;
    $: if (cell.state == "queued") {
        last_height = height;
    } else if (cell.state == "idle") {
        last_height = 0;
    }
    onMount(() => {
        last_height = height;
    });

    // output components
    import ErrorOutput from "./output_components/ErrorOutput.svelte";
    import HtmlOutput from "./output_components/HTMLOutput.svelte";
    import ImageOutput from "./output_components/ImageOutput.svelte";
    import MarkdownOutput from "./output_components/MarkdownOutput.svelte";
    import TextOutput from "./output_components/TextOutput.svelte";
</script>

<div
    class="flex items-start h-auto w-full justify-center align-stretch mt-1 overflow-y-auto"
    style=" max-height: 616px; 
    min-height: {last_height}px; 
    {cell.state == 'queued' ? 'opacity: 0.5' : ''}"
    bind:clientHeight={height}
>
    <div class="flex h-full w-6" style="margin-right:7px" />
    <div
        class="w-full h-auto bg-transparent px-1 pl-1 py-0.5 shadow-inner shadow-zinc-100/50 dark:shadow-vs-dark
             border border-zinc-100 dark:border-neutral-800 rounded float-bottom mt-0.25 cursor-default pointer-events-auto"
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
