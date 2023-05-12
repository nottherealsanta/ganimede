<script>
    import {
        cells,
        id_map,
        pc_graph,
        _resize_ancestors,
        sync_cell_properties,
        pn_graph,
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

    import { get_mouse_pos_on_cell } from "../utils/cell_utils.js";
    $: mouse_pos_on_cell = get_mouse_pos_on_cell(cell, $mouse_pos);

    let inside_div_height = 0;
    $: min_height = inside_div_height + 10;
    $: cell.height = min_height;

    let inside_div_width = 0;
    $: cell.width = inside_div_width + 10;

    import mouse_pos from "../stores/mouse.js";

    // drag handle
    // let drag_handle = null;
    // import { is_mouse_inside_this_div } from "../utils/cell_utils.js";
    // let dragging = false;
    // let dh_clicked = {
    //     x: 0,
    //     y: 0,
    // };
    // function drag_handle_mousedown(e) {
    //     if (e.button === 0) {
    //         e.preventDefault();
    //         dragging = true;
    //         dh_clicked = {
    //             x: $mouse_pos.x - cell.left,
    //             y: $mouse_pos.y - cell.top,
    //             children: [],
    //         };
    //     }
    // }
    // function drag_handle_mousemove(e) {
    //     if (dragging) {
    //         $cells[$id_map[cell_id]].top = $mouse_pos.y - dh_clicked.y;
    //         $cells[$id_map[cell_id]].left = $mouse_pos.x - dh_clicked.x;

    //         for (let child of dh_clicked.children) {
    //             let child_cell = $cells[$id_map[child.id]];
    //             child_cell.top = $mouse_pos.y - child.y;
    //             child_cell.left = $mouse_pos.x - child.x;
    //             $cells[$id_map[child.id]] = child_cell;
    //         }
    //     }
    // }
    // function drag_handle_mouseup(e) {
    //     dragging = false;

    //     // snap to previous
    //     let prev_cell_id = $pn_graph[cell_id];
    //     let prev_cell = $cells[$id_map[prev_cell_id]];
    //     if (prev_cell) {
    //         if (
    //             cell.top - (prev_cell.top + prev_cell.height) < 50 &&
    //             cell.left - prev_cell.left < 50 &&
    //             cell.left - prev_cell.left > -50
    //         ) {
    //             cell.top = prev_cell.top + prev_cell.height + 5;
    //             cell.left = prev_cell.left;
    //         }
    //         $cells[$id_map[cell_id]] = cell;
    //     }

    //     sync_cell_properties(cell_id);
    // }

    import NewCellToolbar from "../components/cell_components/NewCellToolbar.svelte";
    import CellToolbar from "../components/cell_components/CellToolbar.svelte";
</script>

<div
    style="
    top: {cell.top}px; left: {cell.left}px; 
    height: {cell.height}px;
    width: {cell.width}px; 
    min-width: max-content;
    "
    class=" cell
    bg-white dark:bg-vs-dark
    absolute rounded-lg
    border
    border-gray-300 dark:border-neutral-800
    shadow-md shadow-zinc-300 dark:shadow-neutral-900/50
    flex overflow-visible p-1 cursor-default
    "
    id="cell"
    bind:this={div}
>
    <!-- cell toolbar -->
    <!-- {#if cell.execution_count !== null}
        <div
            class="absolute top-2 right-3 text-[10px] text-gray-700/50 dark:text-neutral-400/50 z-10"
        >
            {cell.execution_count}
        </div>
    {/if} -->
    <!-- this inside div exists to get the height and width of the content -->
    <div
        style="height: fit-content; width: fit-content;"
        bind:clientHeight={inside_div_height}
        bind:clientWidth={inside_div_width}
    >
        <slot />
    </div>
    <!-- drag handle -->
    {#if mouse_pos_on_cell}
        <NewCellToolbar {cell_id} />
        <CellToolbar {cell_id} />
    {/if}
</div>
