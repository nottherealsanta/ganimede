<script lang="ts">
    export let cell_id;
    import { notebook, id_map } from "../../stores/notebook";
    $: cell_type = $notebook["cells"][$id_map[cell_id]].type;

    // code outputs
    $: outputs = $notebook["cells"][$id_map[cell_id]].outputs;

    // markdown
    // import { marked } from "marked";
    // $: if (cell_type === "markdown") {
    //     let source = $notebook["cells"][$id_map[cell_id]].source;
    //     outputs = marked(source.join("\n"));
    // }
</script>

<div class="flex items-start h-auto w-full justify-center align-stretch mt-1">
    <div class="flex h-full w-6" style="margin-right:7px" />
    <div
        class="w-full h-auto bg-transparent px-1 py-0.5 shadow-inner shadow-zinc-100/50 dark:shadow-vs-dark
                    border border-zinc-100 dark:border-neutral-800 rounded float-bottom mt-0.25 cursor-default
                    max-h-52 overflow-y-auto overflow-x-auto pointer-events-none
                    "
    >
        {#if cell_type === "code" && outputs}
            {#each outputs as output}
                <div
                    class="w-fit h-auto
                bg-transparent
                hover:bg-gray-100 dark:hover:bg-zinc-700
                pl-1 pr-1 pt-0.5 pb-0.5
                rounded
                whitespace-pre-line
                overflow-hidden
                text-xs
                "
                >
                    <!-- TODO: each output types as components -->
                    {#if output["output_type"] === "stream"}
                        {output["text"].join(" ")}
                    {/if}
                    {#if output["output_type"] === "execute_result"}
                        {output["data"]["text/plain"]}
                    {/if}
                    {#if output["output_type"] === "display_data"}
                        {output["data"]["text/markdown"]}
                    {/if}
                    {#if output["output_type"] === "error"}
                        {output["ename"]}
                        {output["evalue"]}
                        {output["traceback"]}
                    {/if}
                </div>
            {/each}
        {:else if cell_type === "markdown"}
            {@html outputs}
        {/if}
    </div>
</div>
