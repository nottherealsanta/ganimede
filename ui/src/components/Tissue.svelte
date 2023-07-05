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

    onMount(() => {
        tissue_div.setAttribute("cell_id", cell_id);
        $html_elements[cell_id] = tissue_div;
        $html_elements[cell_id].setAttribute("dragging", "false");

        // tissue_div.setAttribute("items", JSON.stringify(items));
    });

    let dragging = false;
    let dragging_began = false;

    let dh_clicked = {
        x: 0,
        y: 0,
    };

    let drag_cell_pos = {
        x: null,
        y: null,
    };

    let dnd_line = null;
    let dnd_box = null;

    function drag_handle_mousedown(e) {
        if (e.button === 0) {
            e.stopPropagation();
            e.preventDefault();
            dragging = true;
            dh_clicked = {
                x: $mouse_pos.x - $cells[$id_map[cell_id]].left,
                y: $mouse_pos.y - $cells[$id_map[cell_id]].top,
            };
            drag_cell_pos = {
                x: $cells[$id_map[cell_id]].left,
                y: $cells[$id_map[cell_id]].top,
            };
            $html_elements[cell_id].setAttribute("dragging", "true");
        }
    }
    function drag_handle_mousemove(e) {
        if (dragging) {
            dragging_began = true;
            e.preventDefault();
            e.stopPropagation();

            $cells[$id_map[cell_id]].top = $mouse_pos.y - dh_clicked.y;
            $cells[$id_map[cell_id]].left = $mouse_pos.x - dh_clicked.x;

            // set cell position while dragging
            drag_cell_pos = {
                x: $mouse_pos.x - dh_clicked.x,
                y: $mouse_pos.y - dh_clicked.y,
            };

            // top of
            const elements_under = document.elementsFromPoint(
                e.clientX,
                e.clientY
            );
            let cell_under = elements_under.filter(
                (el) =>
                    el.classList.contains("cell") &&
                    el.getAttribute("cell_id") !== cell_id
            )[0];
            let tissue_under = elements_under.filter(
                (el) =>
                    el.classList.contains("tissue") &&
                    el.getAttribute("cell_id") !== cell_id
            )[0];
            const dragzone_under = elements_under.filter((el) =>
                el.classList.contains("dropzone")
            )[0];
            const dragzone_under_tissue = dragzone_under
                ? dragzone_under.parentNode.parentNode
                : undefined;

            // if elements_under has dragzone that's cellid = cell_id
            if (cell_under == undefined && tissue_under !== undefined) {
                if (
                    (dragzone_under !== undefined &&
                        dragzone_under.getAttribute("cell_id") !==
                            tissue_under.getAttribute("cell_id")) ||
                    dragzone_under == undefined
                ) {
                    if (tissue_under.getAttribute("cell_id") !== cell_id) {
                        cell_under = tissue_under;
                    }
                }
            }
            // when moving fast, the tissue might want to be next to it's children
            if (cell_under !== undefined) {
                if (
                    $pc_graph[cell_id] &&
                    $pc_graph[cell_id].includes(
                        cell_under.getAttribute("cell_id")
                    )
                ) {
                    cell_under = undefined;
                }
            }

            // check if on cell
            if (cell_under) {
                let _bounding_rect = {
                    top: cell_under.offsetTop,
                    left: cell_under.offsetLeft,
                    width: cell_under.getBoundingClientRect().width,
                    height: cell_under.getBoundingClientRect().height,
                    bottom:
                        cell_under.offsetTop +
                        cell_under.getBoundingClientRect().height,
                };
                if (dnd_line === null) {
                    dnd_line = document.createElement("div");
                    dnd_line.style.position = "absolute";
                    dnd_line.style.height = "3px";
                    dnd_line.style.borderRadius = "5px";
                    dnd_line.style.backgroundColor = "#29BFFF";

                    dnd_line.style.left = _bounding_rect.left.toString() + "px";
                    dnd_line.style.width =
                        _bounding_rect.width.toString() + "px";

                    dnd_line.setAttribute(
                        "cell_id",
                        cell_under.getAttribute("cell_id")
                    );
                    document.body.appendChild(dnd_line);
                }

                // if mouse is on bottom/top half of cell
                if (dnd_line) {
                    if (
                        $mouse_pos.y >
                        _bounding_rect.top + _bounding_rect.height / 2
                    ) {
                        // draw pointer on bottom
                        dnd_line.style.top =
                            _bounding_rect.bottom.toString() + "px";
                        dnd_line.setAttribute("position", "bottom");
                    } else {
                        // draw pointer on top
                        dnd_line.style.top =
                            _bounding_rect.top.toString() + "px";
                        dnd_line.setAttribute("position", "top");
                    }
                }

                // if moved to another cell
                if (
                    dnd_line &&
                    dnd_line.getAttribute("cell_id") !==
                        cell_under.getAttribute("cell_id")
                ) {
                    // if node in document.body then remove
                    if (dnd_line.parentNode === document.body) {
                        document.body.removeChild(dnd_line);
                    }
                    dnd_line = null;
                }
            }
            // if mouse_on_cell is null
            if (cell_under === undefined) {
                if (dnd_line) {
                    document.body.removeChild(dnd_line);
                    dnd_line = null;
                }
            }

            // check if on tissue
            if (
                dragzone_under &&
                dragzone_under_tissue.getAttribute("cell_id") !== cell_id
            ) {
                let _bounding_rect = {
                    top:
                        dragzone_under.offsetTop +
                        dragzone_under_tissue.offsetTop +
                        2,
                    left:
                        dragzone_under.offsetLeft +
                        dragzone_under_tissue.offsetLeft +
                        2,
                    width: dragzone_under.getBoundingClientRect().width + 4,
                    height: dragzone_under.getBoundingClientRect().height + 2,
                };

                if (dnd_box === null) {
                    dnd_box = document.createElement("div");
                    dnd_box.style.position = "absolute";
                    dnd_box.style.top = _bounding_rect.top.toString() + "px";
                    dnd_box.style.left = _bounding_rect.left.toString() + "px";
                    dnd_box.style.width =
                        _bounding_rect.width.toString() + "px";
                    dnd_box.style.height =
                        _bounding_rect.height.toString() + "px";
                    dnd_box.style.backgroundColor = "#29BFFF11";
                    dnd_box.style.border = "2px solid #29BFFF";
                    dnd_box.style.borderRadius = "0px 0px 5px 0px";
                    dnd_box.style.pointerEvents = "none";

                    dnd_box.setAttribute(
                        "cell_id",
                        dragzone_under.getAttribute("cell_id")
                    );

                    document.body.appendChild(dnd_box);
                }

                // if moved to another tissue
                if (
                    dnd_box &&
                    dnd_box.getAttribute("cell_id") !==
                        dragzone_under.getAttribute("cell_id")
                ) {
                    // if node in document.body then remove
                    if (dnd_box.parentNode === document.body) {
                        document.body.removeChild(dnd_box);
                    }
                    dnd_box = null;
                }
            } else if (dragzone_under === undefined) {
                if (dnd_box) {
                    document.body.removeChild(dnd_box);
                    dnd_box = null;
                }
            }
        }
    }
    function drag_handle_mouseup(e) {
        if (dragging && dragging_began) {
            // TODO: move snap separetly

            dh_clicked = {
                x: 0,
                y: 0,
            };

            $cells[$id_map[cell_id]].top = drag_cell_pos.y;
            $cells[$id_map[cell_id]].left = drag_cell_pos.x;

            drag_cell_pos = {
                x: null,
                y: null,
            };

            $html_elements[cell_id].setAttribute("dragging", "false");

            if (dnd_line) {
                let dnd_cell_id = dnd_line.getAttribute("cell_id");
                let dnd_parent = $cp_graph[dnd_cell_id];

                let cell_parent = $cp_graph[cell_id];
                // let cell_loc = [...$pc_graph[cell_parent]].indexOf(cell_id);
                // check if cell is in some parent
                if (cell_parent) {
                    var cell_loc = [...$pc_graph[cell_parent]].indexOf(cell_id);
                }

                // insert cell after dnd_cell_id
                let position = dnd_line.getAttribute("position");

                // copy pc_graph - to enforce reactivity (`set` updates cp_graph)
                let pc_graph_copy = JSON.parse(JSON.stringify($pc_graph));

                // remove cell from parent
                if (cell_parent) {
                    pc_graph_copy[cell_parent].splice(cell_loc, 1);
                }

                // add to next to dnd_cell_id
                let dnd_cell_loc_pos;
                if (dnd_parent) {
                    if (position === "bottom") {
                        dnd_cell_loc_pos =
                            pc_graph_copy[dnd_parent].indexOf(dnd_cell_id) + 1;
                    } else if (position === "top") {
                        dnd_cell_loc_pos =
                            pc_graph_copy[dnd_parent].indexOf(dnd_cell_id);
                    }
                    pc_graph_copy[dnd_parent].splice(
                        dnd_cell_loc_pos,
                        0,
                        cell_id
                    );
                } else {
                    // dragging onto a non-parent cell
                    // TODO: now only snaps to bottom, make it snap to top as well
                    $cells[$id_map[cell_id]].left =
                        $cells[$id_map[dnd_cell_id]].left;

                    $cells[$id_map[cell_id]].top =
                        $cells[$id_map[dnd_cell_id]].top +
                        $cells[$id_map[dnd_cell_id]].height +
                        10;
                }

                // update pc_graph
                pc_graph.set(pc_graph_copy);
            } else if (dnd_box) {
                // add to the end of the tissue/parent
                let dnd_cell_id = dnd_box.getAttribute("cell_id");

                // if dropped on the same parent, preserve order
                if ($cp_graph[cell_id] !== dnd_cell_id) {
                    // copy pc_graph - to enforce reactivity (`set` updates cp_graph)
                    let pc_graph_copy = JSON.parse(JSON.stringify($pc_graph));

                    let cell_parent = $cp_graph[cell_id];

                    // remove cell from parent
                    if (cell_parent) {
                        pc_graph_copy[cell_parent].splice(
                            [...$pc_graph[cell_parent]].indexOf(cell_id),
                            1
                        );
                    }

                    // add to the end of the tissue/parent
                    pc_graph_copy[dnd_cell_id].push(cell_id);

                    // update pc_graph
                    pc_graph.set(pc_graph_copy);
                }
            } else {
                // remove from parent
                let cell_parent = $cp_graph[cell_id];
                if (cell_parent) {
                    let cell_loc = [...$pc_graph[cell_parent]].indexOf(cell_id);

                    // copy pc_graph - to enforce reactivity (`set` updates cp_graph)
                    let pc_graph_copy = JSON.parse(JSON.stringify($pc_graph));

                    // remove cell from parent
                    pc_graph_copy[cell_parent].splice(cell_loc, 1);

                    // update pc_graph
                    pc_graph.set(pc_graph_copy);
                }
            }

            if (dnd_line) {
                document.body.removeChild(dnd_line);
                dnd_line = null;
            }
            if (dnd_box) {
                document.body.removeChild(dnd_box);
                dnd_box = null;
            }

            // sync
            // sync_cell_properties(cell_id);
        }
        dragging = false;
        dragging_began = false;
    }

    $: if (
        $cp_graph[cell_id] &&
        $html_elements[$cp_graph[cell_id]] &&
        !dragging
    ) {
        // find loc of cell_id in $pc_graph[$cp_graph[cell_id]]
        let cell_loc = [...$pc_graph[$cp_graph[cell_id]]].indexOf(cell_id);
        if (cell_loc === 0) {
            let parent_cell = $cells[$id_map[$cp_graph[cell_id]]];
            let top_pos =
                parent_cell.top +
                $html_elements[$cp_graph[cell_id]].querySelector("#title")
                    .clientHeight +
                6;
            let left_pos = parent_cell.left + 9;
            if ($cells[$id_map[cell_id]].top !== top_pos) {
                $cells[$id_map[cell_id]].top = top_pos;
            }
            if ($cells[$id_map[cell_id]].left !== left_pos) {
                $cells[$id_map[cell_id]].left = left_pos;
            }
        } else {
            let prev_cell_id = [...$pc_graph[$cp_graph[cell_id]]][cell_loc - 1];
            if (
                (prev_cell_id in $pc_graph &&
                    $html_elements[prev_cell_id].getAttribute("dragging") ===
                        "false") ||
                !(prev_cell_id in $pc_graph)
            ) {
                let prev_cell = $cells[$id_map[prev_cell_id]];
                let top_pos = prev_cell.top + prev_cell.height + 8;

                if ($cells[$id_map[cell_id]].top !== top_pos) {
                    $cells[$id_map[cell_id]].top = top_pos;
                }
                if ($cells[$id_map[cell_id]].left !== prev_cell.left) {
                    $cells[$id_map[cell_id]].left = prev_cell.left;
                }
            }
        }
    }

    let tissue_height = 0;
    let tissue_width = 0;

    // sum of clienteHeight of all children = tissue_height
    $: if ($pc_graph[cell_id] && $html_elements[cell_id]) {
        tissue_height = $pc_graph[cell_id].reduce((acc, child_cell_id) => {
            return acc + $html_elements[child_cell_id].clientHeight + 8;
        }, 0);
        // max of clientWidth of all children = tissue_width
        tissue_width = $pc_graph[cell_id].reduce((acc, child_cell_id) => {
            return Math.max(acc, $html_elements[child_cell_id].clientWidth + 7);
        }, 0);
    }

    import MarkdownCell from "./MarkdownCell.svelte";
    import PrimeButton from "./cell_components/PrimeButton.svelte";
    import NewCellToolbar from "../components/cell_components/new_cell_toolbar_components/NewCellToolbar.svelte";
</script>

<!-- top:{cell.top}px; left:{cell.left}px;  -->
<div
    class="tissue absolute flex flex-row h-fit w-fit m-0 rounded border border-oli-300 dark:border-oli-500 shadow-md shadow-zinc-300 dark:shadow-neutral-900/50 overflow-visible cursor-default"
    style="
    top: {$cells[$id_map[cell_id]].top}px;
    left: {$cells[$id_map[cell_id]].left}px;
    z-index: {dragging ? 1000 : 0};
    "
    bind:this={tissue_div}
    bind:clientHeight={$cells[$id_map[cell_id]].height}
    bind:clientWidth={$cells[$id_map[cell_id]].width}
>
    <!-- drag handle (left) -->
    <div
        class="w-[7px] pt-1 flex flex-col rounded-l bg-oli-100 dark:bg-oli-600 border-r border-oli-300 dark:border-oli-500 items-center justify-center"
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
            class="flex flex-row bg-oli-100 dark:bg-oli-700 rounded-tr border-b border-oli-300 dark:border-oli-500 pl-1 items-center justify-center cursor-grab active:cursor-grabbing"
            id="title"
            on:mousedown={drag_handle_mousedown}
            on:mouseup={drag_handle_mouseup}
        >
            <PrimeButton {cell_id} />
            <MarkdownCell {cell_id} is_tissue={true} />
        </div>

        <div
            id="dropzone"
            class="dropzone bg-oli-50/30 dark:bg-oli-700/10"
            style="width:{tissue_width}px; height:{tissue_height}px; 
            min-width:{tissue_div
                ? tissue_div.querySelector('#title').clientWidth
                : 100}px;
            min-height:50px;"
            {cell_id}
        />
    </div>
    {#if !$cp_graph[cell_id]}
        <NewCellToolbar {cell_id} />
    {/if}
    <!-- <div
        class="absolute top-0 left-0 w-full h-full"
        style="pointer-events: none;"
    >
        {cell_id}
    </div> -->
</div>

<!-- {#if $pc_graph[cell_id]}
    {#each $pc_graph[cell_id] as child_cell_id}
        {#if $cells[$id_map[child_cell_id]].type === "markdown" && child_cell_id in $pc_graph}
            <svelte:self cell_id={child_cell_id} />
        {:else}
            <Cell cell_id={child_cell_id} />
        {/if}
    {/each}
{/if} -->

<svelte:window
    on:mousemove={drag_handle_mousemove}
    on:mouseup={drag_handle_mouseup}
/>
