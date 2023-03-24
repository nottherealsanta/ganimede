<script lang="ts">
    import CodeCell from "./CodeCell.svelte";
    import MarkdownCell from "./MarkdownCell.svelte";
    import Edges from "./utility_components/Edges.svelte";

    import { notebook, cells, id_map } from "../stores/notebook";
    function set_locs() {
        // Iterate through each cell
        for (let cell_index = 0; cell_index < $cells.length; cell_index++) {
            // If the cell is not the first cell
            if (cell_index - 1 >= 0) {
                // Get the ids of all previous cells
                let previous_ids = $cells[cell_index].metadata.gm.previous;
                // Get the actual cells from the ids
                let previous_cells = previous_ids.map(
                    (id) => $cells[$id_map[id]]
                );
                // Get the heights of all previous cells
                let previous_heights = previous_cells.map(
                    (cell) => cell.metadata.gm.height
                );
                // Get the top positions of all previous cells
                let previous_tops = previous_cells.map(
                    (cell) => cell.metadata.gm.top
                );
                // Get the bottom positions of all previous cells
                let previous_bottoms = previous_tops.map(
                    (top, i) => top + previous_heights[i]
                );
                // Get the maximum bottom position of all previous cells
                let max_bottom = Math.max(...previous_bottoms);
                // Set the top position of the current cell to be 10 pixels
                // below the maximum bottom position of all previous cells
                $cells[cell_index].metadata.gm.top = max_bottom + 5;
            } else {
                // If the cell is the first cell, set its top position to 100
                $cells[cell_index].metadata.gm.top = 100;
            }
            // Set the left position of the current cell to 100
            $cells[cell_index].metadata.gm.left = 100;
        }
    }

    // run set_loc 1 second after the notebook is loaded
    // setTimeout(set_locs, 100);
    // TODO: only if notebook is new to gm
    // notebook.get().then(setTimeout(set_locs, 200));
</script>

<div class="notebook">
    {#if Object.keys($notebook).length !== 0}
        <!-- nodes -->
        {#each $notebook["cells"] as cell}
            {#if cell.cell_type === "code" && cell.metadata.gm.parent === null}
                <CodeCell cell_id={cell.id} />
            {/if}
            {#if cell.cell_type === "markdown" && cell.metadata.gm.parent === null}
                <MarkdownCell cell_id={cell.id} />
            {/if}
        {/each}
        <!-- edges -->
        {#each $notebook["cells"] as cell}
            {#each cell.metadata.gm.next as next_id}
                <Edges current_cell_id={cell.id} {next_id} />
            {/each}
        {/each}
    {/if}
</div>

<style>
    .notebook {
        display: flex;
    }
</style>
