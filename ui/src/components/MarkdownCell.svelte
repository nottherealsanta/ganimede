<script lang="ts">
    import Cell from "./Cell.svelte";
    import Tissue from "./Tissue.svelte";
    import { id_map, cells, heading_levels } from "../stores/notebook";

    export let cell_id;

    $: cell = $cells[$id_map[cell_id]];
    $: is_heading = $heading_levels[cell_id];

    import { Editor, rootCtx, defaultValueCtx } from "@milkdown/core";
    import { commonmark } from "@milkdown/preset-commonmark";

    function editor(dom) {
        Editor.make()
            .config((ctx) => {
                ctx.set(rootCtx, dom);
                ctx.set(defaultValueCtx, cell.source.join(""));
            })
            .use(commonmark)
            .create();
    }
</script>

{#if is_heading}
    <Tissue {cell_id}>
        <div
            use:editor
            class="bg-gray-50 dark:bg-neutral-800 w-full h-fit m-1 rounded"
        />
    </Tissue>
{:else}
    <Cell {cell_id}>
        <div
            use:editor
            class="bg-gray-50 dark:bg-neutral-800 w-fit h-fit m-1 rounded"
        />
    </Cell>
{/if}
