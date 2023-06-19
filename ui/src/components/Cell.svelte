<!-- <script>
    import {
        cells,
        id_map,
        _resize_ancestors,
        sync_cell_properties,
        html_elements,
    } from "../stores/notebook";

    let div = null;

    export let cell_id;
    $: cell = $cells[$id_map[cell_id]];

    import { onMount } from "svelte";
    onMount(() => {
        div.setAttribute("cell_id", cell_id);
        $html_elements[cell_id] = div;
        setTimeout(() => {
            sync_cell_properties(cell_id);
        }, 500);
    });

    // import { get_mouse_pos_on_cell } from "../utils/cell_utils.js";
    // $: mouse_pos_on_cell = get_mouse_pos_on_cell(cell, $mouse_pos);

    let inside_div_height = 0;
    $: min_height = inside_div_height + 10;
    $: cell.height = min_height;

    let inside_div_width = 0;
    $: cell.width = inside_div_width + 10;

    import mouse_pos from "../stores/mouse.js";

    import NewCellToolbar from "../components/cell_components/new_cell_toolbar_components/NewCellToolbar.svelte";
    import CellToolbar from "../components/cell_components/CellToolbar.svelte";
</script>

<div
    style="
top: {cell.top}px; left: {cell.left}px; 
height: {cell.height}px;
width: {cell.width}px; 
min-width: max-content;
    "
    class="cell bg-white dark:bg-vs-dark absolute rounded-md border border-gray-300 dark:border-neutral-800 shadow-md shadow-zinc-300 dark:shadow-neutral-900/50 flex overflow-visible p-1 cursor-default"
    id="cell"
    bind:this={div}
> -->
<!-- this inside div exists to get the height and width of the content -->
<!-- <div
        style="height: fit-content; width: fit-content;"
        bind:clientHeight={inside_div_height}
        bind:clientWidth={inside_div_width}
    >
        <slot />
    </div> -->
<!-- drag handle -->
<!-- {#if mouse_pos_on_cell}
        <NewCellToolbar {cell_id} />
        <CellToolbar {cell_id} />
    {/if} -->
<!-- </div> -->

<script>
    import { onMount } from "svelte";

    export let cell_id;
    let cell_div;

    import { id_map, cells, cp_graph, pn_graph } from "../stores/notebook";
    $: cell = $cells[$id_map[cell_id]];

    onMount(() => {
        cell_div.setAttribute("cell_id", cell_id);
    });

    import CodeCell from "./CodeCell.svelte";
    import MarkdownCell from "./MarkdownCell.svelte";

    // dragging
    import mouse_pos from "../stores/mouse.js";
    let dragging = false;
    let dh_clicked = {
        x: 0,
        y: 0,
    };

    function drag_mousedown(e) {
        if (e.button === 0) {
            e.stopPropagation();
            e.preventDefault();
            dragging = true;
            dh_clicked = {
                x: $mouse_pos.x - cell.left,
                y: $mouse_pos.y - cell.top,
            };
        }
    }

    function drag_mousemove(e) {
        if (dragging) {
            e.preventDefault();
            e.stopPropagation();
            $cells[$id_map[cell_id]].top = $mouse_pos.y - dh_clicked.y;
            $cells[$id_map[cell_id]].left = $mouse_pos.x - dh_clicked.x;
        }
    }

    function drag_mouseup(e) {
        if (dragging) {
            dragging = false;
            // TODO: move snap separetly
            let prev_cell_id = $pn_graph[cell_id];
            let prev_cell = $cells[$id_map[prev_cell_id]];
            if (prev_cell) {
                let d = {
                    x: cell.left,
                    y: cell.top,
                };
                if (
                    cell.top - (prev_cell.top + prev_cell.height) < 100 &&
                    cell.left - prev_cell.left < 50 &&
                    cell.left - prev_cell.left > -50
                ) {
                    cell.top = prev_cell.top + prev_cell.height + 5;
                    cell.left = prev_cell.left;
                }
                $cells[$id_map[cell_id]] = cell;
            }
            dh_clicked = {
                x: 0,
                y: 0,
            };
            // sync_cell_properties(cell_id);
        }
    }
</script>

<div
    class="bg-white w-fit h-fit dark:bg-vs-dark rounded-md border border-gray-300 dark:border-neutral-800 shadow-md shadow-zinc-300 dark:shadow-neutral-900/50 flex overflow-visible p-1 cursor-default pointer-events-none"
    bind:this={cell_div}
    style="
    top:{cell.top}px; left:{cell.left}px;
     {$cp_graph[cell_id] ? '' : 'position:absolute;'}"
    on:mousedown={$cp_graph[cell_id] ? () => {} : drag_mousedown}
    on:mouseup={$cp_graph[cell_id] ? () => {} : drag_mouseup}
    bind:clientHeight={cell.height}
    bind:clientWidth={cell.width}
>
    <div style="height: fit-content; width: fit-content;">
        {#if cell.type === "code"}
            <CodeCell {cell_id} />
        {:else if cell.type === "markdown"}
            <MarkdownCell {cell_id} />
        {/if}
    </div>
</div>

<svelte:window
    on:mousemove={$cp_graph[cell_id] ? () => {} : drag_mousemove}
    on:mouseup={$cp_graph[cell_id] ? () => {} : drag_mouseup}
/>
