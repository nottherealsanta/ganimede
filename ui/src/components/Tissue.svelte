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
        // tissue_div.setAttribute("items", JSON.stringify(items));
    });

    // drag and drop list
    import { dndzone } from "svelte-dnd-action";

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
    import { mouse_on_tissues, dragging_cell_id } from "../stores/mouse.js";

    $: if ($mouse_on_tissues[1]) {
        if (
            $mouse_on_tissues[1].getAttribute("cell_id") == cell_id &&
            dragging_cell_id != null &&
            items.filter((item) => item._id == $dragging_cell_id).length == 0
        ) {
            console.log(
                "tissue",
                cell_id,
                $dragging_cell_id,
                $mouse_on_tissues
            );
            items.push({
                _id: $dragging_cell_id,
                ...$cells[$id_map[$dragging_cell_id]],
            });
        }
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
            $dragging_cell_id = cell_id;
        }
    }

    function drag_handle_mousemove(e) {
        if (dragging) {
            e.preventDefault();
            e.stopPropagation();
            $cells[$id_map[cell_id]].top = $mouse_pos.y - dh_clicked.y;
            $cells[$id_map[cell_id]].left = $mouse_pos.x - dh_clicked.x;

            // if mouse is over the class '.dropzone'
            // then console log
            // console.log(e);
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
            $dragging_cell_id = null;
        }
    }

    // propective child

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
        <!-- dropzone list of children -->
        <div
            class="dropzone pl-4 pt-2 pb-2 pr-2 h-full w-full"
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
                <!-- get index of item -->
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
    {cell_id}
</div>

<svelte:window
    on:mousemove={drag_handle_mousemove}
    on:mouseup={drag_handle_mouseup}
/>
