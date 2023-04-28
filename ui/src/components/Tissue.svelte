<script>
    import {
        cells,
        id_map,
        heading_levels,
        pc_graph,
    } from "../stores/notebook";

    let div = null;

    export let cell_id;
    $: cell = $cells[$id_map[cell_id]];

    $: is_heading = $heading_levels[cell_id];

    import mouse_pos from "../stores/mouse.js";
    import { get_mouse_pos_on_cell } from "../utils/cell_utils.js";
    $: mouse_pos_on_cell = get_mouse_pos_on_cell(cell, $mouse_pos);

    let inside_div_height = 0;
    $: min_height = inside_div_height + 10;
    $: if (cell.height < min_height) {
        cell.height = min_height;
    }

    let inside_div_width = 0;
    $: if (cell.width < inside_div_width) {
        cell.width = inside_div_width + 10;
    }

    // resize
    import {
        detect_cell_edge,
        cell_edge_to_cursor,
        cell_edge_to_resize_fn,
    } from "../utils/cell_utils.js";

    let resize_clicked = {
        at: null,
        x: 0,
        y: 0,
    };

    function resize_mousemove(e) {
        if (resize_clicked.at === null && cell.type !== "code") {
            // hover
            let cell_edge = detect_cell_edge(cell, mouse_pos_on_cell);
            if (cell_edge) {
                div.style.cursor = cell_edge_to_cursor(cell_edge);
            } else {
                div.style.cursor = "default";
            }
        } else {
            // resize_clicked for resize
            [cell.top, cell.left, cell.height, cell.width] =
                cell_edge_to_resize_fn($mouse_pos, resize_clicked, cell);
            if (cell.height < min_height) {
                cell.height = min_height;
            }
            $cells[$id_map[cell_id]] = cell;
        }
    }

    function resize_mousedown(e) {
        if (
            e.button === 0 &&
            e.target.id === "cell" &&
            cell.type !== "code" &&
            !dragging
        ) {
            e.preventDefault();
            resize_clicked = {
                at: detect_cell_edge(cell, mouse_pos_on_cell),
                x: mouse_pos_on_cell.x,
                y: mouse_pos_on_cell.y,
            };
        }
    }

    function resize_mouseup(e) {
        resize_clicked = {
            at: null,
            x: 0,
            y: 0,
        };
    }

    // drag handle
    let drag_handle = null;
    import { is_mouse_inside_this_div } from "../utils/cell_utils.js";
    let dragging = false;
    let dh_clicked = {
        x: 0,
        y: 0,
    };
    function drag_handle_mousedown(e) {
        if (e.button === 0) {
            e.preventDefault();
            dragging = true;
            dh_clicked = {
                x: $mouse_pos.x - cell.left,
                y: $mouse_pos.y - cell.top,
                children: [],
            };

            let children = $pc_graph[cell_id];
            for (let child of children) {
                dh_clicked.children.push({
                    id: child,
                    x: $mouse_pos.x - $cells[$id_map[child]].left,
                    y: $mouse_pos.y - $cells[$id_map[child]].top,
                });
                if ($pc_graph[child]) {
                    children.push(...$pc_graph[child]);
                }
            }
        }
    }
    function drag_handle_mousemove(e) {
        if (dragging) {
            $cells[$id_map[cell_id]].top = $mouse_pos.y - dh_clicked.y;
            $cells[$id_map[cell_id]].left = $mouse_pos.x - dh_clicked.x;

            for (let child of dh_clicked.children) {
                let child_cell = $cells[$id_map[child.id]];
                child_cell.top = $mouse_pos.y - child.y;
                child_cell.left = $mouse_pos.x - child.x;
                $cells[$id_map[child.id]] = child_cell;
            }
        }
    }
    function drag_handle_mouseup(e) {
        dragging = false;
    }

    import NewCellToolbar from "./cell_components/NewCellToolbar.svelte";
</script>

<div
    style="
    top: {cell.top}px; left: {cell.left}px; 
    height: {cell.height}px;
    width: {cell.width}px; 
    min-width: max-content;
    opacity: {dragging ? 0.75 : 1};
    "
    class="
    bg-gray-50/50 dark:bg-neutral-800/30
    absolute rounded-lg
    border-2
    border-gray-500 dark:border-gray-400
    shadow-md shadow-zinc-300 dark:shadow-neutral-900/50
    flex overflow-visible p-1 cursor-default
    "
    id="cell"
    bind:this={div}
    on:mousedown={resize_mousedown}
>
    <!-- this inside div exists to get the height and width of the content -->
    <div
        style="height: fit-content; width: fit-content;"
        bind:clientHeight={inside_div_height}
        bind:clientWidth={inside_div_width}
    >
        <slot />
    </div>
    <NewCellToolbar {cell_id} />
    <!-- drag handle -->
    {#if mouse_pos_on_cell || is_mouse_inside_this_div(drag_handle, $mouse_pos) || dragging}
        {#if $mouse_pos.y - cell.top > 0}
            <div
                style="top:{$mouse_pos.y - cell.top - 10}px; "
                class="absolute bg-transparent w-4 h-5 -left-4 cursor-grab active:cursor-grabbing"
                bind:this={drag_handle}
                on:mousedown={drag_handle_mousedown}
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-4 text-gray-700"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                >
                    <path
                        fill-rule="evenodd"
                        d="M 4 2 a 1 1 0 0 0 0 3 A 1 1 0 0 0 4 2 z z z m 0 7 A 1 1 0 0 0 4 12 A 1 1 0 0 0 4 9 m 0 7 A 1 1 0 0 0 4 19 A 1 1 0 0 0 4 16 m 10 -14 A 1 1 0 0 0 14 5 A 1 1 0 0 0 14 2 m 0 7 A 1 1 0 0 0 14 12 A 1 1 0 0 0 14 9 m 0 7 A 1 1 0 0 0 14 19 A 1 1 0 0 0 14 16"
                        clip-rule="evenodd"
                    />
                </svg>
            </div>
        {/if}
    {/if}
</div>

<svelte:window
    on:mouseup={resize_mouseup}
    on:mousemove={resize_mousemove}
    on:mouseup={drag_handle_mouseup}
    on:mousemove={drag_handle_mousemove}
/>
