<script lang="ts">
    import CodeCell from "./CodeCell.svelte";
    import MarkdownCell from "./MarkdownCell.svelte";
    import Edges from "./utility_components/Edges.svelte";

    import {
        notebook,
        cells,
        id_map,
        np_graph,
        pc_graph,
        heading_levels,
        heading_levels_inv,
        parent_less_cells,
    } from "../stores/notebook";

    function set_locs() {
        let _top = 1000;
        let _left = 5000;
        for (let cell_index = 0; cell_index < $cells.length; cell_index++) {
            $cells[cell_index].top = _top;
            $cells[cell_index].left = _left;
            _top += $cells[cell_index].height + 5;
        }
        //  h6 -> h1, set width, height by looking at children's width, height
        for (let level = 6; level >= 1; level--) {
            for (let cell_id of $heading_levels_inv[level]) {
                let cell = $cells[$id_map[cell_id]];
                let children = $pc_graph[cell_id];
                let width = cell.width;
                let height = cell.height;
                for (let child_id of children) {
                    let child = $cells[$id_map[child_id]];
                    width = Math.max(width, child.width);
                    height += child.height + 5;
                    $cells[$id_map[child_id]].left = cell.left + level * 25;
                }
                cell.width = width + 50;
                cell.height = height + 25;
                $cells[$id_map[cell_id]] = cell;
            }
        }
        // h1 -> h6, set next's top and left
        for (let level = 1; level <= 6; level++) {
            for (let cell_id of $heading_levels_inv[level]) {
                let cell = $cells[$id_map[cell_id]];
                if ($np_graph[cell_id]) {
                    let next = $cells[$id_map[$np_graph[cell_id][0]]];
                    if (next) {
                        let d_top = next.top;
                        let d_left = next.left;
                        next.top = cell.top + cell.height + 5;
                        next.left = cell.left;
                        d_top -= next.top;
                        d_left -= next.left;
                        $cells[$id_map[$np_graph[cell_id][0]]] = next;
                        // move all children by d_top, d_left
                        if ($pc_graph[next.id]) {
                            for (let child_id of $pc_graph[next.id]) {
                                let child = $cells[$id_map[child_id]];
                                child.top -= d_top;
                                child.left -= d_left;
                                $cells[$id_map[child_id]] = child;
                            }
                        }
                    }
                }
            }
        }

        window.scrollTo(5000 - 400, 1000 - 200);
    }

    setTimeout(() => {
        if ($cells.every((cell) => cell.top === 0 && cell.left === 0)) {
            set_locs();
        }
    }, 500);
</script>

<div class="notebook">
    {#if Object.keys($notebook).length !== 0}
        {#each [1, 2, 3, 4, 5, 6] as level}
            {#each $heading_levels_inv[level] as cell_id}
                {#if $cells[$id_map[cell_id]].type === "markdown"}
                    <MarkdownCell {cell_id} />
                {/if}
                {#if $pc_graph[cell_id]}
                    {#each $pc_graph[cell_id] as child_id}
                        {#if $cells[$id_map[child_id]].type === "markdown"}
                            <MarkdownCell cell_id={child_id} />
                        {/if}
                        {#if $cells[$id_map[child_id]].type === "code"}
                            <CodeCell cell_id={child_id} />
                        {/if}
                        {#if $np_graph[child_id]}
                            {#each $np_graph[child_id] as next_id}
                                <Edges current_cell_id={child_id} {next_id} />
                            {/each}
                        {/if}
                    {/each}
                {/if}

                {#if $np_graph[cell_id]}
                    {#each $np_graph[cell_id] as next_id}
                        <Edges current_cell_id={cell_id} {next_id} />
                    {/each}
                {/if}
            {/each}
        {/each}

        {#each $parent_less_cells as cell_id}
            {#if $cells[$id_map[cell_id]].type === "markdown"}
                <MarkdownCell {cell_id} />
            {/if}
            {#if $cells[$id_map[cell_id]].type === "code"}
                <CodeCell {cell_id} />
            {/if}
            {#if $np_graph[cell_id]}
                {#each $np_graph[cell_id] as next_id}
                    <Edges current_cell_id={cell_id} {next_id} />
                {/each}
            {/if}
        {/each}
    {/if}
</div>

<style>
    .notebook {
        display: flex;
        flex-direction: column;
    }
</style>
