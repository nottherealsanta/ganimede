<script lang="ts">
    import { afterUpdate, onMount } from "svelte";

    let div = null;
    export let cell;

    onMount(() => {
        for (let i = 0; i < div.children.length; i++) {
            console.log("div.children[i] :", div.children[i].clientWidth);
            cell.height += div.children[i].clientHeight;
        }
        cell.height += 8; // padding
        cell.height += 2; // border
        // cell.width = div.clientWidth;

        // set cell width after 0.1 seconds
        setTimeout(() => {
            cell.width = div.clientWidth;
        }, 100);
    });

    let inside_div = null;
    let min_height = 0;
    $: if (inside_div) {
        min_height = inside_div.clientHeight + 8 + 2;
        if (cell.height < min_height) {
            cell.height = min_height;
        }
    }

    import mouse_pos from "../stores/mouse.js";
    import {
        detect_cell_edge,
        cell_edge_to_cursor,
        cell_edge_to_resize_fn,
    } from "../utils/cell_utils.js";

    let clicked = {
        at: null,
        x: 0,
        y: 0,
    };

    function mousemove(e) {
        if (clicked.at === null) {
            // hover
            let cell_edge = detect_cell_edge(cell, $mouse_pos);
            if (cell_edge) {
                div.style.cursor = cell_edge_to_cursor(cell_edge);
            } else {
                div.style.cursor = "default";
            }
        } else {
            // clicked for resize
            [cell.top, cell.left, cell.height, cell.width] =
                cell_edge_to_resize_fn($mouse_pos, clicked, cell);
            if (cell.height < min_height) {
                cell.height = min_height;
            }
        }
    }

    function mousedown(e) {
        if (e.button === 0 && e.target.id === "cell") {
            e.preventDefault();
            clicked = {
                at: detect_cell_edge(cell, $mouse_pos),
                x: $mouse_pos.x - cell.left,
                y: $mouse_pos.y - cell.top,
            };
        }
    }

    function mouseup(e) {
        clicked = {
            at: null,
            x: 0,
            y: 0,
        };
    }

    import NewCellToolbar from "../components/cell_components/NewCellToolbar.svelte";
</script>

<div
    style="
    top: {cell.top}px; left: {cell.left}px; 
    height: {cell.height}px;
    width: {cell.width}px; 
    min-width: max-content;"
    class="
    bg-white dark:bg-vs-dark
    absolute rounded-lg
    border border-gray-300 dark:border-neutral-800
    shadow-md shadow-zinc-300 dark:shadow-neutral-900/50
    flex overflow-visible p-1 cursor-move"
    id="cell"
    bind:this={div}
    on:mousedown={mousedown}
>
    <div style="height: fit-content; " bind:this={inside_div}>
        <slot />
    </div>
    <NewCellToolbar />
</div>

<svelte:window on:mouseup={mouseup} on:mousemove={mousemove} />
