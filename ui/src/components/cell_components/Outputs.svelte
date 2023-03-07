<script lang="ts">
    export let cell_id;
    import { notebook, id_map } from "../../stores/notebook";
    $: outputs = $notebook["cells"][$id_map[cell_id]].outputs;
</script>

<div class="outputs">
    {#each outputs as output}
        <div class="output">
            <!-- TODO: each output types as components -->
            {#if output["output_type"] === "stream"}
                {output["text"]}
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
</div>

<style>
    .outputs {
        width: auto;
        height: fit-content;
        background-color: transparent;
        border: solid 1px rgba(0, 0, 0, 0.065);
        border-radius: 5px;
        float: bottom;
        margin-top: 1px;
        padding: 2px 3px 2px 4px;
        cursor: default;
        /* box-shadow: -1px 0px 2px 1px rgba(0, 0, 0, 0.048); */

        max-height: 200px;
        overflow-y: auto;

        max-width: 500px;
        overflow-x: auto;
    }

    .output {
        background-color: rgba(255, 255, 255, 0);
        width: fit-content;
        height: fit-content;
        padding: 3px 4px 3px 4px;
        margin: 1px 0px 1px 0px;
        border-radius: 5px;
        /* white-space: pre; */
        overflow: hidden;
    }
    .output:hover {
        background-color: rgba(0, 0, 0, 0.08);
    }

    /* dark mode */
    @media (prefers-color-scheme: dark) {
        .outputs {
            color: #fff;
        }
        .output {
            background-color: rgba(0, 0, 0, 0.02);
        }
    }
</style>
