<script>
    import { onMount } from "svelte";

    export let cell_id;
    let cell_div;

    import {
        id_map,
        cells,
        cp_graph,
        pn_graph,
        html_elements,
        pc_graph,
    } from "../stores/notebook";

    // $: cell = $cells[$id_map[cell_id]];

    // let isMounted = false;
    onMount(() => {
        console.log("onMount", cell_id);
        $html_elements[cell_id] = cell_div;
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
                x: $mouse_pos.x - $cells[$id_map[cell_id]].left,
                y: $mouse_pos.y - $cells[$id_map[cell_id]].top,
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
            // let prev_cell_id = $pn_graph[cell_id];
            // let prev_cell = $cells[$id_map[prev_cell_id]];
            // if (prev_cell) {
            //     let d = {
            //         x: cell.left,
            //         y: cell.top,
            //     };
            //     if (
            //         cell.top - (prev_cell.top + prev_cell.height) < 100 &&
            //         cell.left - prev_cell.left < 50 &&
            //         cell.left - prev_cell.left > -50
            //     ) {
            //         cell.top = prev_cell.top + prev_cell.height + 5;
            //         cell.left = prev_cell.left;
            //     }
            //     $cells[$id_map[cell_id]] = cell;
            // }
            dh_clicked = {
                x: 0,
                y: 0,
            };
            // sync_cell_properties(cell_id);
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
                .clientHeight +
            5;
        let left_pos = parent_cell.left + 25 + 12;
        if ($cells[$id_map[cell_id]].top !== top_pos) {
            $cells[$id_map[cell_id]].top = top_pos;
        }
        if ($cells[$id_map[cell_id]].left !== left_pos) {
            $cells[$id_map[cell_id]].left = left_pos;
        }
    }
</script>

<div
    class="bg-white absolute w-fit h-fit dark:bg-vs-dark rounded-md border border-gray-300 dark:border-neutral-800 shadow-md shadow-zinc-300 dark:shadow-neutral-900/50 flex overflow-visible p-1 cursor-default"
    bind:this={cell_div}
    style="
    top: {$cells[$id_map[cell_id]].top}px; 
    left: {$cells[$id_map[cell_id]].left}px;
    z-index: {dragging ? 99 : 0};
    "
    on:mousedown={drag_mousedown}
    on:mouseup={drag_mouseup}
    bind:clientHeight={$cells[$id_map[cell_id]].height}
    bind:clientWidth={$cells[$id_map[cell_id]].width}
>
    <div style="height: fit-content; width: fit-content;">
        {#if $cells[$id_map[cell_id]].type === "code"}
            <CodeCell {cell_id} />
        {:else if $cells[$id_map[cell_id]].type === "markdown"}
            <MarkdownCell {cell_id} />
        {/if}
    </div>
</div>

<svelte:window on:mousemove={drag_mousemove} on:mouseup={drag_mouseup} />
