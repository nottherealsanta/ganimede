<script>
    import Cell from "./Cell.svelte";
    import Edges from "./utility_components/Edges.svelte";
    import { dndzone } from "svelte-dnd-action";

    import {
        cells,
        id_map,
        pc_graph,
        cp_graph,
        np_graph,
        parent_less_cells,
        heading_levels_inv,
        notebook,
    } from "../stores/notebook";
    import Tissue from "./Tissue.svelte";
</script>

{#if $cells !== undefined}
    {#each $cells.map((cell) => cell.id) as cell_id}
        {#if $cells[$id_map[cell_id]].type === "markdown" && cell_id in $pc_graph}
            <Tissue {cell_id} />
        {:else}
            <Cell {cell_id} />
        {/if}
        {#if $np_graph[cell_id] && !$cp_graph[cell_id]}
            {#each $np_graph[cell_id] as next_id}
                <Edges current_cell_id={cell_id} {next_id} />
            {/each}
        {/if}
    {/each}
{/if}
