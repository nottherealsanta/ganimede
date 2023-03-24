<script lang="ts">
    export let cell_id;
    import { notebook, id_map } from "../../stores/notebook";
    $: cell_type = $notebook["cells"][$id_map[cell_id]].cell_type;

    // code outputs
    $: outputs = $notebook["cells"][$id_map[cell_id]].outputs;

    // markdown
    import { marked } from "marked";
    $: if (cell_type === "markdown") {
        let source = $notebook["cells"][$id_map[cell_id]].source;
        outputs = marked(source.join("\n"));
    }
</script>

<div class="outputs">
    {#if cell_type === "code" && outputs}
        {#each outputs as output}
            <div class="output">
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

<style>
    .outputs {
        width: auto;
        height: fit-content;
        background-color: transparent;
        border: solid 1px rgba(0, 0, 0, 0.065);
        border-radius: 4px;
        float: bottom;
        margin-top: 1px;
        padding: 2px 3px 2px 4px;
        cursor: default;
        /* box-shadow: -1px 0px 2px 1px rgba(0, 0, 0, 0.048); */

        max-height: 200px;
        overflow-y: auto;

        max-width: 616px;
        overflow-x: auto;
    }
    .outputs::-webkit-scrollbar {
        width: 5px;
    }

    .output {
        background-color: rgba(255, 255, 255, 0);
        width: fit-content;
        height: fit-content;
        padding: 3px 4px 3px 4px;
        margin: 1px 0px 1px 0px;
        border-radius: 3px;
        white-space: pre-line;
        overflow: hidden;
        font-size: 12px;
    }
    .output:hover {
        background-color: rgba(0, 0, 0, 0.08);
    }

    /* dark mode */
    @media (prefers-color-scheme: dark) {
        .outputs {
            color: #fff;
            border: solid 1px rgba(255, 255, 255, 0.065);
        }
        .output {
            background-color: rgba(0, 0, 0, 0.02);
        }
        .output:hover {
            background-color: rgba(255, 255, 255, 0.08);
        }
    }
</style>
