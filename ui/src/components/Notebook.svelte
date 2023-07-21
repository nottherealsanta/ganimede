<script>
    // import Cell from "./Cell.svelte";
    // import Edges from "./utility_components/Edges.svelte";
    // import { dndzone } from "svelte-dnd-action";

    // import {
    //     cells,
    //     id_map,
    //     pc_graph,
    //     cp_graph,
    //     np_graph,
    //     parent_less_cells,
    //     heading_levels_inv,
    // } from "../stores/notebook";
    // import Tissue from "./Tissue.svelte";
    // import { onMount } from "svelte";

    import {
        cells,
        ydoc,
        cp_graph,
        pc_graph,
        html_elements,
    } from "../stores/_notebook";

    function get_cell(id) {
        return ydoc.getMap(id);
    }

    function align_parent_less_cells() {
        console.log(">>align_parent_less_cells");
        let top = 5000;
        let left = 5000;
        for (let cell_id of parent_less_cells) {
            get_cell(cell_id).set("top", top);
            top += $html_elements[cell_id].offsetHeight + 10;
            get_cell(cell_id).set("left", left);
        }
        // 
    }

    // wait for $cell to be defined
    let aligned = false;
    $: if ($cells !== undefined && $html_elements !== undefined && !aligned ) {
        aligned = true;
        // call align_parent_less_cells() after 1 second
        // if (!(get_cell($cells[0]).get("top") === 0)){
        
        // setTimeout(align_parent_less_cells, 1000);
        // }
        // window.scrollTo(4900, 4900)
    }

    $: parent_less_cells = $cells
        .filter((cell) => !$cp_graph[cell])
        .map((cell) => cell);
    $: console.log(">>parent_less_cells:", parent_less_cells);

    // Components
    import Cell from "./Cell.svelte";
    import Tissue from "./Tissue.svelte";

    // ---------- zoom
    import { zoom, set_zoom } from "../stores/zoom";
    import { onMount } from "svelte";

    // add event listeners
    onMount(() => {
        window.addEventListener("wheel", (event) => {
            set_zoom(event);
        }, { passive: false });
    });

</script>

<!-- {#if $cells !== undefined}
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
{/if} -->

<!-- {#if $cells.empty === false} -->
<!-- {console.log(">>cells:", $cells)} -->
{#each $cells as cell_id}
    {#if ydoc.getMap(cell_id)}
        {#if cell_id in $pc_graph}
            <Tissue {cell_id} />
        {:else}
            <Cell {cell_id} />
        {/if}
    {/if}
{/each}
