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
                $cells[$id_map[cell_id]].top = top;
                top += $cells[$id_map[cell_id]].height + 10;
                $cells[$id_map[cell_id]].left = left;
            }
        }
        window.scrollTo(4900, 4900);
    }

    // wait for $cell to be defined
    let aligned = false;
    $: if ($cells !== undefined && !aligned) {
        // align_parent_less_cells();
        aligned = true;
        // call align_parent_less_cells() after 1 second
        setTimeout(align_parent_less_cells, 1000);
    }

    // reorder $cells to render parent first then children
    // parent child realtionship is adjancency list: $pc_graph
    let render_order = [];
    $: if ($cells !== undefined) {
        render_order = JSON.parse(JSON.stringify($cells)).map(
            (cell) => cell.id
        );
        // console.log("before", render_order);
        // reorder to render parent first then children
        const visited = new Set();
        const stack = [];
        const topologicalSort = (cell_id) => {
            visited.add(cell_id);
            if ($pc_graph[cell_id]) {
                for (let child_id of $pc_graph[cell_id]) {
                    if (!visited.has(child_id)) {
                        topologicalSort(child_id);
                    }
                }
            }
            stack.push(cell_id);
        };
        for (let cell_id of render_order) {
            if (!visited.has(cell_id)) {
                topologicalSort(cell_id);
            }
        }

        render_order = stack.reverse();
        // render_order.reverse();
        // console.log("after", render_order);
        // console.log("pc_graph", $pc_graph);
    }
    // sort
</script>

{#if $cells !== undefined}
    {#each [1, 2, 3, 4, 5, 6] as level}
        {#each $heading_levels_inv[level] as cell_id}
            <Tissue {cell_id} />
            {#if $np_graph[cell_id] && !$cp_graph[cell_id]}
                {#each $np_graph[cell_id] as next_id}
                    <Edges current_cell_id={cell_id} {next_id} />
                {/each}
            {/if}
        {/each}
    {/each}

    {#each $cells.map((cell) => cell.id) as cell_id}
        {#if !($cells[$id_map[cell_id]].type === "markdown" && cell_id in $pc_graph)}
            <Cell {cell_id} />
        {/if}
    {/each}

    <!-- {@debug render_order} -->
{/if}
