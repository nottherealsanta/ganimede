<!-- <script>
    import {
        cells,
        id_map,
        heading_levels,
        pc_graph,
        sync_cell_properties,
        _resize_ancestors,
        pn_graph,
        html_elements,
    } from "../stores/notebook";

    let tissue_div = null;
    let tissue_selector_div = null;

    export let cell_id;
    $: cell = $cells[$id_map[cell_id]];

    import { onMount } from "svelte";
    onMount(() => {
        tissue_selector_div.setAttribute("cell_id", cell_id);
        tissue_div.setAttribute("cell_id", cell_id);
        $html_elements[cell_id] = tissue_div;

        if (!(cell_id in $pc_graph) || $pc_graph[cell_id].length === 0) {
            console.log("Adding cell to parent-less cells");
            $cells[$id_map[cell_id]].height = 150;
            $cells[$id_map[cell_id]].width = 250;
        }

        setTimeout(() => {
            sync_cell_properties(cell_id);
        }, 500);
    });

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
    // $: if (cell.width < inside_div_width) {
    //     cell.width = inside_div_width + 10;
    // }

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

    function resize_mousedown(e) {
        let at = detect_cell_edge(cell, mouse_pos_on_cell);
        if (e.button === 0 && at !== null) {
            e.preventDefault();
            e.stopPropagation();

            resize_clicked = {
                at: at,
                x: mouse_pos_on_cell.x,
                y: mouse_pos_on_cell.y,
            };
            //  get x and y bound by looking at tissue's children
            let children = $pc_graph[cell_id];
            let x_bounds = [cell.left + cell.width, cell.left];
            let y_bounds = [cell.top + cell.height, cell.top];
            if (children) {
                for (let child of children) {
                    let child_cell = $cells[$id_map[child]];
                    x_bounds[0] = Math.min(x_bounds[0], child_cell.left);
                    x_bounds[1] = Math.max(
                        x_bounds[1],
                        child_cell.left + child_cell.width
                    );
                    y_bounds[0] = Math.min(y_bounds[0], child_cell.top);
                    y_bounds[1] = Math.max(
                        y_bounds[1],
                        child_cell.top + child_cell.height
                    );
                }
                x_bounds[0] -= 25;
                x_bounds[1] += 25;
                y_bounds[0] -= min_height;
                y_bounds[1] += 25;
            }
            resize_clicked.x_bounds = x_bounds;
            resize_clicked.y_bounds = y_bounds;
        }
    }

    function resize_mousemove(e) {
        if (resize_clicked.at === null) {
            // hover
            let cell_edge = detect_cell_edge(cell, mouse_pos_on_cell);
            if (cell_edge) {
                tissue_div.style.cursor = cell_edge_to_cursor(cell_edge);
            } else {
                tissue_div.style.cursor = "default";
            }
        } else {
            // resize_clicked for resize
            [cell.top, cell.left, cell.height, cell.width] =
                cell_edge_to_resize_fn($mouse_pos, resize_clicked, cell);
            if (cell.height < min_height) {
                cell.height = min_height;
            }

            // bound
            if (cell.left + cell.width < resize_clicked.x_bounds[1]) {
                cell.width = resize_clicked.x_bounds[1] - cell.left;
            }
            if (cell.left > resize_clicked.x_bounds[0]) {
                cell.left = resize_clicked.x_bounds[0];
                cell.width = resize_clicked.x_bounds[1] - cell.left;
            }
            if (cell.top + cell.height < resize_clicked.y_bounds[1]) {
                cell.height = resize_clicked.y_bounds[1] - cell.top;
            }
            if (cell.top > resize_clicked.y_bounds[0]) {
                cell.top = resize_clicked.y_bounds[0];
                cell.height = resize_clicked.y_bounds[1] - cell.top;
            }
            $cells[$id_map[cell_id]] = cell;
        }
        e.stopPropagation();
    }

    function resize_mouseup(e) {
        if (e.button === 0 && resize_clicked.at !== null) {
            e.preventDefault();
            resize_clicked = {
                at: null,
                x: 0,
                y: 0,
            };
            console.log("resize mouseup : ", cell_id);
            sync_cell_properties(cell_id);
        }
    }

    // drag handle
    let drag_handle = null;
    let dragging = false;
    let dh_clicked = {
        x: 0,
        y: 0,
        children: [],
    };

    function get_drag_handle_clicked() {
        return {
            x: $mouse_pos.x - cell.left,
            y: $mouse_pos.y - cell.top,
            children: get_drag_handle_children(),
        };
    }

    function get_drag_handle_children() {
        let children = [];
        if ($pc_graph[cell_id]) {
            for (let child of $pc_graph[cell_id]) {
                children.push({
                    id: child,
                    x: $mouse_pos.x - $cells[$id_map[child]].left,
                    y: $mouse_pos.y - $cells[$id_map[child]].top,
                });
                children.push(...get_drag_handle_children_recursive(child));
            }
        }
        return children;
    }

    function get_drag_handle_children_recursive(cell_id) {
        let children = [];
        if ($pc_graph[cell_id]) {
            for (let child of $pc_graph[cell_id]) {
                children.push({
                    id: child,
                    x: $mouse_pos.x - $cells[$id_map[child]].left,
                    y: $mouse_pos.y - $cells[$id_map[child]].top,
                });
                children.push(...get_drag_handle_children_recursive(child));
            }
        }
        return children;
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
            e.stopPropagation();
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
        if (dragging) {
            dragging = false;
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
                    d.x = cell.left - d.x;
                    d.y = cell.top - d.y;
                    for (let child of dh_clicked.children) {
                        let child_cell = $cells[$id_map[child.id]];
                        child_cell.top += d.y;
                        child_cell.left += d.x;
                        $cells[$id_map[child.id]] = child_cell;
                    }
                }
                $cells[$id_map[cell_id]] = cell;
            }
            dh_clicked = {
                x: 0,
                y: 0,
                children: [],
            };
            sync_cell_properties(cell_id);
        }
    }

    // mouse on tissue
    let mouse_on_tissue = false;
    function mouse_on_tissue_enter(e) {
        mouse_on_tissue = true;
    }
    function mouse_on_tissue_leave(e) {
        mouse_on_tissue = false;
    }

    import NewCellToolbar from "./cell_components/new_cell_toolbar_components/NewCellToolbar.svelte";
    import CellToolbar from "./cell_components/CellToolbar.svelte";
    import Drag from "./cell_components/Icons/drag.svelte";
</script> -->

<!-- <div
    style="
    top: {cell.top}px; left: {cell.left}px; 
    height: {cell.height}px;
    width: {cell.width}px; 
    min-width: max-content;
    {dragging ? 'border: 2px solid #49B0F9;' : ''}
    "
    class="tissue bg-gray-50/50 dark:bg-neutral-800/30 absolute rounded-md border-l-2 border-r-2 border-t-2 border-b-2 border-[#212529] dark:border-gray-400 shadow-md shadow-zinc-300 dark:shadow-neutral-900/50 flex overflow-visible cursor-default"
    id="tissue"
    bind:this={tissue_div}
    on:mouseleave={mouse_on_tissue_leave}
    on:mouseover={mouse_on_tissue_enter}
    on:mousedown={resize_mousedown}
    on:focus={mouse_on_tissue_enter}
    on:blur={mouse_on_tissue_leave}
>
    <div class="flex flex-row w-full">
        <div
            style={dragging ? "background-color: #49B0F9;" : ""}
            class=" w-1 h-full bg-[#212529] dark:bg-gray-300 rounded-tl rounded-bl"
            bind:this={tissue_selector_div}
            id="tissue_selector"
        />
        <div
            class="w-full bg-[#212529]"
            style="height: fit-content;"
            bind:clientHeight={inside_div_height}
            bind:clientWidth={inside_div_width}
        >
            <slot />
        </div>
    </div>
    {#if mouse_pos_on_cell && mouse_on_tissue}
        <CellToolbar {cell_id} />
        {#if $mouse_pos.y - cell.top > 0}
            <NewCellToolbar {cell_id} />
            <div
                style="top:{$mouse_pos.y - cell.top - 10}px; "
                class="absolute bg-transparent w-5 h-8 -left-4 cursor-grab active:cursor-grabbing fill-neutral-500 dark:fill-neutral-400"
                bind:this={drag_handle}
                on:mousedown={drag_handle_mousedown}
                on:mouseup={drag_handle_mouseup}
            >
                <Drag />
            </div>
        {/if}
    {/if}
</div> -->
<!-- 
<svelte:window
    on:mousemove={resize_mousemove}
    on:mousemove={drag_handle_mousemove}
    on:mouseup={resize_mouseup}
    on:mouseup={drag_handle_mouseup}
/> -->

<script>
    import { dndzone } from "svelte-dnd-action";

    import Cell from "./Cell.svelte";

    import {
        cells,
        id_map,
        heading_levels,
        pc_graph,
        sync_cell_properties,
        _resize_ancestors,
        parent_less_cells,
        pn_graph,
        html_elements,
        cp_graph,
    } from "../stores/notebook";
    import { onMount } from "svelte";
    import mouse_pos from "../stores/mouse.js";

    export let cell_id;
    let tissue_div;
    $: cell = $cells[$id_map[cell_id]];

    onMount(() => {
        tissue_div.setAttribute("cell_id", cell_id);
    });

    // drag and drop list
    let items = [];
    let set_items = false;
    $: if ($pc_graph[cell_id] && !set_items) {
        let children = [...$pc_graph[cell_id]];
        items = [];
        for (let child of children) {
            items.push({ _id: child, ...$cells[$id_map[child]] });
        }
        set_items = true;
    }

    function handleDndConsider(e) {
        console.log("> consider", e.detail.info.id, e.detail.info.trigger);

        items = e.detail.items;
    }
    function handleDndFinalize(e) {
        console.log("> finalize", e.detail.info.id, e.detail.info.trigger);
        let final_items = e.detail.items;

        // dragging cell/sub-tissue out to canvas
        if (e.detail.info.trigger == "droppedOutsideOfAny") {
            // dragging outside removes it from the items
            final_items = final_items.filter(
                (item) => item._id != e.detail.info.id
            );
            // set mouse pos as loc after drag
            let x = $cells[$id_map[e.detail.info.id]];
            x.top = $mouse_pos.y - 50;
            x.left = $mouse_pos.x - 50;
            $cells[$id_map[e.detail.info.id]] = x;
            console.log(e.detail.info.id, "dragged out");
        }
        items = final_items;
        $pc_graph[cell_id] = items.map((item) => item._id);
    }

    // tissue mouse
    let mouse_on_tissue = false;
    function tissue_mouseenter(e) {
        mouse_on_tissue = true;
    }
    function tissue_mouseleave(e) {
        mouse_on_tissue = false;
    }

    // drag handle
    import MarkdownCell from "./MarkdownCell.svelte";
    let dragging = false;
    let dh_clicked = {
        x: 0,
        y: 0,
        children: [],
    };

    function get_drag_handle_clicked() {
        return {
            x: $mouse_pos.x - cell.left,
            y: $mouse_pos.y - cell.top,
        };
    }

    // function get_drag_handle_children() {
    //     let children = [];
    //     if ($pc_graph[cell_id]) {
    //         for (let child of $pc_graph[cell_id]) {
    //             children.push({
    //                 id: child,
    //                 x: $mouse_pos.x - $cells[$id_map[child]].left,
    //                 y: $mouse_pos.y - $cells[$id_map[child]].top,
    //             });
    //             children.push(...get_drag_handle_children_recursive(child));
    //         }
    //     }
    //     return children;
    // }

    // function get_drag_handle_children_recursive(cell_id) {
    //     let children = [];
    //     if ($pc_graph[cell_id]) {
    //         for (let child of $pc_graph[cell_id]) {
    //             children.push({
    //                 id: child,
    //                 x: $mouse_pos.x - $cells[$id_map[child]].left,
    //                 y: $mouse_pos.y - $cells[$id_map[child]].top,
    //             });
    //             children.push(...get_drag_handle_children_recursive(child));
    //         }
    //     }
    //     return children;
    // }

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
                children: [],
            };
            sync_cell_properties(cell_id);
        }
    }

    import PrimeButton from "./cell_components/PrimeButton.svelte";
</script>

<div
    class="tissue flex flex-row h-fit bg-gray-50/50 dark:bg-neutral-800/30 rounded-md border-l-2 border-r-2 border-t-2 border-b-2 border-[#212529] dark:border-gray-400 shadow-md shadow-zinc-300 dark:shadow-neutral-900/50 overflow-visible cursor-default"
    style="
    top:{cell.top}px; left:{cell.left}px; 
    {$cp_graph[cell_id] ? '' : 'position:absolute;'}
    {$cp_graph[cell_id] ? 'width:100%;' : 'width:fit-content;'}
    "
    on:mouseover={tissue_mouseenter}
    on:mouseout={tissue_mouseleave}
    on:focus={tissue_mouseenter}
    on:blur={tissue_mouseleave}
    bind:this={tissue_div}
    bind:clientHeight={cell.height}
    bind:clientWidth={cell.width}
>
    <!-- drag handle (left) -->
    <div
        class="flex bg-[#212529] dark:bg-neutral-400 w-2 fill-neutral-500 dark:fill-neutral-400"
    >
        {#if !$cp_graph[cell_id]}
            <div
                class="w-full h-full cursor-grab active:cursor-grabbing"
                on:mousedown={drag_handle_mousedown}
                on:mouseup={drag_handle_mouseup}
            />
        {/if}
    </div>
    <div class="flex flex-col w-full h-full">
        <!-- title -->
        <div
            class="flex flex-row bg-neutral-100/30 dark:bg-neutral-400/30 p-1 justify-start items-start cursor-grab active:cursor-grabbing"
            on:mousedown={drag_handle_mousedown}
            on:mouseup={drag_handle_mouseup}
        >
            <PrimeButton {cell_id} />
            <MarkdownCell {cell_id} is_tissue={true} />
        </div>
        <!-- list of children -->
        <div
            class="pl-4 pt-2 pb-2 pr-2 h-full w-full"
            use:dndzone={{
                items,
                dropTargetStyle: {
                    outline: "rgba(73, 176, 249, 0.7) solid 2px",
                },
            }}
            on:consider={handleDndConsider}
            on:finalize={handleDndFinalize}
        >
            {#each items as item (item._id)}
                <div class="my-1">
                    {#if $pc_graph[item.id]}
                        <svelte:self cell_id={item.id} />
                    {:else}
                        <Cell cell_id={item.id} />
                    {/if}
                </div>
            {/each}
        </div>
    </div>
</div>
<svelte:window
    on:mousemove={drag_handle_mousemove}
    on:mouseup={drag_handle_mouseup}
/>
