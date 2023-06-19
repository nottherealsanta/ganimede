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
    } from "../stores/notebook";
    import { onMount } from "svelte";
    import mouse_pos from "../stores/mouse.js";

    export let cell_id;
    let tissue_div;
    $: cell = $cells[$id_map[cell_id]];

    onMount(() => {
        tissue_div.setAttribute("cell_id", cell_id);
    });

    let children = [...$pc_graph[cell_id]] || [];
    let mouseYCoordinate = null; // pointer y coordinate within client
    let distanceTopGrabbedVsPointer = null;

    let draggingItem = null;
    // let draggingItemId = null;
    let draggingItemIndex = null;

    let hoveredItemIndex = null;

    $: {
        if (
            draggingItemIndex != null &&
            hoveredItemIndex != null &&
            draggingItemIndex != hoveredItemIndex
        ) {
            // swap items
            [children[draggingItemIndex], children[hoveredItemIndex]] = [
                children[hoveredItemIndex],
                children[draggingItemIndex],
            ];
            // $pc_graph[cell_id] = children;

            // balance
            draggingItemIndex = hoveredItemIndex;
        }
    }

    // // drag and drop list
    // let items = [];
    // let set_items = false;
    // $: if ($pc_graph[cell_id] && !set_items) {
    //     let children = [...$pc_graph[cell_id]];
    //     items = [];
    //     for (let child of children) {
    //         items.push({ _id: child, ...$cells[$id_map[child]] });
    //     }
    //     set_items = true;
    // }

    // function handleDndConsider(e) {
    //     console.log("> consider", e.detail.info.id, e.detail.info.trigger);

    //     items = e.detail.items;
    // }
    // function handleDndFinalize(e) {
    //     console.log("> finalize", e.detail.info.id, e.detail.info.trigger);
    //     let final_items = e.detail.items;

    //     // dragging cell/sub-tissue out to canvas
    //     if (e.detail.info.trigger == "droppedOutsideOfAny") {
    //         // dragging outside removes it from the items
    //         final_items = final_items.filter(
    //             (item) => item._id != e.detail.info.id
    //         );
    //         // set mouse pos as loc after drag
    //         let x = $cells[$id_map[e.detail.info.id]];
    //         x.top = $mouse_pos.y - 50;
    //         x.left = $mouse_pos.x - 50;
    //         $cells[$id_map[e.detail.info.id]] = x;
    //         console.log(e.detail.info.id, "dragged out");
    //     }
    //     items = final_items;
    //     $pc_graph[cell_id] = items.map((item) => item._id);
    // }

    // tissue mouse
    let mouse_on_tissue = false;
    function tissue_mouseenter(e) {
        mouse_on_tissue = true;
    }
    function tissue_mouseleave(e) {
        mouse_on_tissue = false;
    }

    // drag handle
    let dragging = false;
    let dh_clicked = {
        x: 0,
        y: 0,
    };

    function get_drag_handle_clicked() {
        return {
            x: $mouse_pos.x - cell.left,
            y: $mouse_pos.y - cell.top,
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

    import MarkdownCell from "./MarkdownCell.svelte";
    import PrimeButton from "./cell_components/PrimeButton.svelte";
</script>

<!-- top:{cell.top}px; left:{cell.left}px;  -->
<div
    class="tissue flex flex-row h-fit bg-gray-50/50 dark:bg-neutral-800/30 rounded-md border-l-2 border-r-2 border-t-2 border-b-2 border-[#212529] dark:border-gray-400 shadow-md shadow-zinc-300 dark:shadow-neutral-900/50 overflow-visible cursor-default"
    style="
    {$cp_graph[cell_id] ? '' : 'position:absolute;'}
    {$cp_graph[cell_id] ? 'width:100%;' : 'width:fit-content;'}
    {$cp_graph[cell_id] ? '' : 'top:' + cell.top + 'px;'}
    {$cp_graph[cell_id] ? '' : 'left:' + cell.left + 'px;'}
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
        <div class="flex flex-col w-full h-full p-1 pl-3">
            {#each children as child_id, index}
                <div
                    class="my-1 h-fit w-fit cursor-grab active:cursor-grabbing"
                    style="opacity: {draggingItem == child_id ? 0 : 1};"
                    draggable={true}
                    on:dragstart={(e) => {
                        mouseYCoordinate = e.clientY;
                        //console.log('dragstart', mouseYCoordinate);

                        draggingItem = child_id;
                        draggingItemIndex = index;
                        // draggingItemId = e.target.getAttribute("cell_id"); // makes item invisible

                        distanceTopGrabbedVsPointer =
                            e.target.getBoundingClientRect().y - e.clientY;
                        console.log(
                            "dragstart",
                            e.target.getBoundingClientRect().y,
                            e.clientY,
                            distanceTopGrabbedVsPointer
                        );

                        /* invisible drag image */
                        e.dataTransfer.setDragImage(new Image(), 0, 0);
                    }}
                    on:drag={(e) => {
                        mouseYCoordinate = e.clientY;
                    }}
                    on:dragover={(e) => {
                        hoveredItemIndex = index;
                    }}
                    on:dragend={(e) => {
                        draggingItem = null;
                        // draggingItemId = null; // makes item visible
                        hoveredItemIndex = null; // prevents instant swap
                        draggingItemIndex = null;
                        console.log("dragend", mouseYCoordinate);
                    }}
                >
                    {#if $pc_graph[child_id]}
                        <svelte:self cell_id={child_id} />
                    {:else}
                        <Cell cell_id={child_id} />
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
