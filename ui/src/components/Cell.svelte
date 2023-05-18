<script>
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

    import { get_mouse_pos_on_cell } from "../utils/cell_utils.js";
    $: mouse_pos_on_cell = get_mouse_pos_on_cell(cell, $mouse_pos);

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
>
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
