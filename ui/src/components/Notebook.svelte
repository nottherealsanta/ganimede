<script lang="ts">
    import CodeCell from "./CodeCell.svelte";
    import MarkdownCell from "./MarkdownCell.svelte";
    import Edges from "./utility_components/Edges.svelte";

    import { notebook, cells, id_map } from "../stores/notebook";

    function set_locs() {
        // Iterate through each cell
        for (let cell_index = 0; cell_index < $cells.length; cell_index++) {
            // If the cell is not the first cell and the height of the cell is 0
            if (cell_index - 1 >= 0 && $cells[cell_index].height === 0) {
                // Get the ids of all previous cells
                let previous_ids = $cells[cell_index].previous;
                // Get the actual cells from the ids
                let previous_cells = previous_ids.map(
                    (id) => $cells[$id_map[id]]
                );
                // Get the heights of all previous cells
                let previous_heights = previous_cells.map(
                    (cell) => cell.height
                );
                // Get the top positions of all previous cells
                let previous_tops = previous_cells.map((cell) => cell.top);
                // Get the bottom positions of all previous cells
                let previous_bottoms = previous_tops.map(
                    (top, i) => top + previous_heights[i]
                );
                // Get the maximum bottom position of all previous cells
                let max_bottom = Math.max(...previous_bottoms);
                // Set the top position of the current cell to be 10 pixels
                // below the maximum bottom position of all previous cells
                $cells[cell_index].top = max_bottom + 5;
            } else {
                // If the cell is the first cell, set its top position to 100
                $cells[cell_index].top = 100;
            }
            // Set the left position of the current cell to 100
            $cells[cell_index].left = 100;
        }
    }

    // if all the cells have 0 as top and left
    // then set the locations
    // setTimeout(() => {
    //     if ($cells.every((cell) => cell.top === 0 && cell.left === 0)) {
    //         set_locs();
    //     }
    // }, 500);

    import Cell from "./Cell.svelte";
</script>

<div class="notebook">
    {#if Object.keys($notebook).length !== 0}
        <!-- nodes -->
        {#each $notebook["cells"] as cell}
            {#if cell.cell_type === "code"}
                <CodeCell cell_id={cell.id} />
            {/if}
            {#if cell.cell_type === "markdown"}
                <!-- <MarkdownCell cell_id={cell.id} /> -->
            {/if}
        {/each}
        <!-- edges -->
        <!-- {#each $notebook["cells"] as cell}
        {#each cell.next as next_id}
            <Edges current_cell_id={cell.id} {next_id} />
        {/each}
    {/each} -->
    {/if}
    <!-- <Cell /> -->
</div>

<style>
    .notebook {
        display: flex;
        flex-direction: column;
    }
</style>
