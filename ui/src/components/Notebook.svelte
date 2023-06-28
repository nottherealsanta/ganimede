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

    // if all the parent_less_cells are 0 in top and left
    // place them one after another in a column
    // if(
    //     $parent_less_cells.length > 0 &&
    //     $parent_less_cells.every((cell_id) => {
    //         return (
    //             $cells[id_map[cell_id]].top === 0 &&
    //             $cells[id_map[cell_id]].left === 0
    //         );
    //     })
    // ) {
    //     let top = 0;
    //     for (let cell_id of $parent_less_cells) {
    //         $cells[id_map[cell_id]].top = top;
    //         top += $cells[id_map[cell_id]].height + 10;
    //     }
    // }

    function align_parent_less_cells() {
        if (
            $parent_less_cells.length > 0 &&
            $parent_less_cells.every((cell_id) => {
                return (
                    $cells[$id_map[cell_id]].top === 0 &&
                    $cells[$id_map[cell_id]].left === 0
                );
            })
        ) {
            let top = 5000;
            let left = 5000;
            for (let cell_id of $parent_less_cells) {
                console.log(Object.values($cells[$id_map[cell_id]]));
                $cells[$id_map[cell_id]].top = top;
                top += $cells[$id_map[cell_id]].height + 10;
                $cells[$id_map[cell_id]].left = left;
            }
        }
        window.scrollTo(4500, 4800);
    }

    // wait for $cell to be defined
    let aligned = false;
    $: if ($cells !== undefined && !aligned) {
        // align_parent_less_cells();
        aligned = true;
        // call align_parent_less_cells() after 1 second
        setTimeout(align_parent_less_cells, 1000);
    }
</script>

{#if Object.keys($notebook).length !== 0}
    {#each [1, 2, 3, 4, 5, 6] as level}
        {#each $heading_levels_inv[level] as cell_id}
            <Tissue {cell_id} />
            {#if $pc_graph[cell_id]}
                {#each $pc_graph[cell_id] as child_id}
                    {#if !(child_id in $pc_graph)}
                        <Cell cell_id={child_id} />
                    {/if}
                {/each}
            {/if}
        {/each}
    {/each}
    {#each $parent_less_cells as cell_id}
        {#if !$cp_graph[cell_id] && !(cell_id in $pc_graph)}
            <Cell {cell_id} />
        {/if}
        {#if $np_graph[cell_id]}
            {#each $np_graph[cell_id] as next_id}
                <Edges current_cell_id={cell_id} {next_id} />
            {/each}
        {/if}
    {/each}
{/if}

<!-- {#if $cells !== undefined}
    {#each $cells.map((cell) => cell.id) as cell_id}
        {#if $cells[$id_map[cell_id]].type === "markdown" && cell_id in $pc_graph}
            <Tissue {cell_id} />
        {:else}
            <Cell {cell_id} />
        {/if}

    {/each}
{/if} -->
