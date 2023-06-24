<script>
    import Cell from "./Cell.svelte";

    import {
        cells,
        id_map,
        pc_graph,
        sync_cell_properties,
        _resize_ancestors,
        pn_graph,
        cp_graph,
        html_elements,
    } from "../stores/notebook";
    import { onMount } from "svelte";
    import mouse_pos from "../stores/mouse.js";

    export let cell_id;
    let tissue_div = null;

    let tissue_height = 0;
    let tissue_width = 0;

    $: _children = $pc_graph[cell_id];
    // sum of clienteHeight of all children = tissue_height
    $: tissue_height =
        _children.reduce((acc, child_cell_id) => {
            return acc + $cells[$id_map[child_cell_id]].height;
        }, 0) + 25;
    // max of clientWidth of all children = tissue_width
    $: tissue_width =
        _children.reduce((acc, child_cell_id) => {
            return Math.max(acc, $cells[$id_map[child_cell_id]].width);
        }, 0) + 50;

    onMount(() => {
        tissue_div.setAttribute("cell_id", cell_id);
        $html_elements[cell_id] = tissue_div;

        // tissue_div.setAttribute("items", JSON.stringify(items));
    });

    let dragging = false;
    let dh_clicked = {
        x: 0,
        y: 0,
    };

    function get_drag_handle_clicked() {
        return {
            x: $mouse_pos.x - $cells[$id_map[cell_id]].left,
            y: $mouse_pos.y - $cells[$id_map[cell_id]].top,
        };
    }

    function drag_handle_mousedown(e) {
        if (e.button === 0) {
            e.stopPropagation();
            e.preventDefault();
            dragging = true;
            dh_clicked = get_drag_handle_clicked();
        }
    }

    function drag_handle_mousemove(e) {
        if (dragging) {
            e.preventDefault();
            e.stopPropagation();
            $cells[$id_map[cell_id]].top = $mouse_pos.y - dh_clicked.y;
            $cells[$id_map[cell_id]].left = $mouse_pos.x - dh_clicked.x;
        }
    }

    function drag_handle_mouseup(e) {
        if (dragging) {
            dragging = false;
            let prev_cell_id = $pn_graph[cell_id];
            let prev_cell = $cells[$id_map[prev_cell_id]];
            if (prev_cell) {
                let cell = $cells[$id_map[cell_id]];
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
            sync_cell_properties(cell_id);
        }
    }

    $: if ($pn_graph[cell_id] && !dragging) {
        let prev_cell_id = $pn_graph[cell_id][0];
        let prev_cell = $cells[$id_map[prev_cell_id]];
        let top_pos = prev_cell.top + prev_cell.height + 5;

        if ($cells[$id_map[cell_id]].top !== top_pos) {
            $cells[$id_map[cell_id]].top = top_pos;
        }
        if ($cells[$id_map[cell_id]].left !== prev_cell.left) {
            $cells[$id_map[cell_id]].left = prev_cell.left;
        }
    } else if (
        $cp_graph[cell_id] &&
        $html_elements[$cp_graph[cell_id]] &&
        !dragging
    ) {
        let parent_cell = $cells[$id_map[$cp_graph[cell_id]]];
        let top_pos =
            parent_cell.top +
            $html_elements[$cp_graph[cell_id]].querySelector("#title")
                .clientHeight;
        let left_pos = parent_cell.left + 25 + 12;
        if ($cells[$id_map[cell_id]].top !== top_pos) {
            $cells[$id_map[cell_id]].top = top_pos;
        }
        if ($cells[$id_map[cell_id]].left !== left_pos) {
            $cells[$id_map[cell_id]].left = left_pos;
        }
    }

    import MarkdownCell from "./MarkdownCell.svelte";
    import PrimeButton from "./cell_components/PrimeButton.svelte";
</script>

<!-- top:{cell.top}px; left:{cell.left}px;  -->
<div
    class="tissue absolute flex flex-row h-fit w-fit bg-gray-50/50 dark:bg-neutral-800/30 rounded-md border-l-2 border-r-2 border-t-2 border-b-2 border-[#212529] dark:border-gray-400 shadow-md shadow-zinc-300 dark:shadow-neutral-900/50 overflow-visible cursor-default"
    style="
    top:{$cells[$id_map[cell_id]].top}px; 
    left:{$cells[$id_map[cell_id]].left}px;
    "
    bind:this={tissue_div}
    bind:clientHeight={$cells[$id_map[cell_id]].height}
    bind:clientWidth={$cells[$id_map[cell_id]].width}
>
    <!-- drag handle (left) -->
    <div
        class="flex bg-[#212529] dark:bg-neutral-400 w-2 fill-neutral-500 dark:fill-neutral-400"
    >
        <div
            class="w-full h-full cursor-grab active:cursor-grabbing"
            on:mousedown={drag_handle_mousedown}
            on:mouseup={drag_handle_mouseup}
        />
    </div>
    <div class="flex flex-col w-full h-full">
        <!-- title -->
        <div
            class="flex flex-row bg-neutral-100/30 dark:bg-neutral-400/30 p-1 justify-start items-start cursor-grab active:cursor-grabbing"
            id="title"
        >
            <PrimeButton {cell_id} />
            <MarkdownCell {cell_id} is_tissue={true} />
        </div>

        <div
            class="bg-transparent"
            style="width:{tissue_width}px; height:{tissue_height}px;"
        />

        <!-- dropzone list of children -->
        <!-- list of children -->

        <!-- {#each $pc_graph[cell_id] as child_cell_id}
            <div class="my-1">
                {#if $pc_graph[child_cell_id]}
                    <svelte:self cell_id={child_cell_id} />
                {:else}
                    <Cell cell_id={child_cell_id} />
                {/if}
            </div>
        {/each} -->
    </div>
</div>

<svelte:window
    on:mousemove={drag_handle_mousemove}
    on:mouseup={drag_handle_mouseup}
/>
