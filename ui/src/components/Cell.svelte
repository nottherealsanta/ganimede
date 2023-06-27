<script>
    import { onMount } from "svelte";

    export let cell_id;
    let cell_div;

    import {
        id_map,
        cells,
        cp_graph,
        pn_graph,
        np_graph,
        html_elements,
        pc_graph,
    } from "../stores/notebook";

    onMount(() => {
        cell_div.setAttribute("cell_id", cell_id);
        $html_elements[cell_id] = cell_div;
    });

    import CodeCell from "./CodeCell.svelte";
    import MarkdownCell from "./MarkdownCell.svelte";

    // dragging
    import mouse_pos from "../stores/mouse.js";

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

    function drag_mousedown(e) {
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
        }
    }

    function drag_mousemove(e) {
        if (dragging) {
            dragging_began = true;
            e.preventDefault();
            e.stopPropagation();

            // set cell position while dragging
            drag_cell_pos = {
                x: $mouse_pos.x - dh_clicked.x,
                y: $mouse_pos.y - dh_clicked.y,
            };

            if (!$cp_graph[cell_id]) {
                $cells[$id_map[cell_id]].top = $mouse_pos.y - dh_clicked.y;
                $cells[$id_map[cell_id]].left = $mouse_pos.x - dh_clicked.x;
            }

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
            let tissue_under = elements_under.filter((el) =>
                el.classList.contains("tissue")
            )[0];
            const dragzone_under = elements_under.filter((el) =>
                el.classList.contains("dropzone")
            )[0];
            const dragzone_under_tissue = dragzone_under
                ? dragzone_under.parentNode.parentNode
                : undefined;

            if (cell_under == undefined && tissue_under !== undefined) {
                if (
                    (dragzone_under !== undefined &&
                        dragzone_under.getAttribute("cell_id") !==
                            tissue_under.getAttribute("cell_id")) ||
                    dragzone_under == undefined
                ) {
                    cell_under = tissue_under;
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
            if (dragzone_under) {
                let _bounding_rect = {
                    top:
                        dragzone_under.offsetTop +
                        dragzone_under_tissue.offsetTop +
                        2,
                    left:
                        dragzone_under.offsetLeft +
                        dragzone_under_tissue.offsetLeft +
                        2,
                    width: dragzone_under.getBoundingClientRect().width,
                    height: dragzone_under.getBoundingClientRect().height,
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

    function drag_mouseup(e) {
        if (dragging && dragging_began) {
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

            if (dnd_line) {
                let dnd_cell_id = dnd_line.getAttribute("cell_id");
                let dnd_parent = $cp_graph[dnd_cell_id];
                let dnd_cell_loc = [...$pc_graph[dnd_parent]].indexOf(
                    dnd_cell_id
                );

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

                if (position === "bottom") {
                    // insert after dnd_cell_id
                    pc_graph_copy[dnd_parent].splice(
                        dnd_cell_loc + 1,
                        0,
                        cell_id
                    );
                } else if (position === "top") {
                    // insert before dnd_cell_id
                    pc_graph_copy[dnd_parent].splice(dnd_cell_loc, 0, cell_id);
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

                // if cell is in some parent
                // if there is any movement
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
            console.log("dragging mouse up end");
        }
        dragging_began = false;
        dragging = false;
    }

    $: if (
        $cp_graph[cell_id] &&
        !dragging &&
        $html_elements[$cp_graph[cell_id]]
    ) {
        // find loc of cell_id in $pc_graph[$cp_graph[cell_id]]
        let cell_loc = [...$pc_graph[$cp_graph[cell_id]]].indexOf(cell_id);
        if (cell_loc === 0) {
            let parent_cell = $cells[$id_map[$cp_graph[cell_id]]];
            let top_pos =
                parent_cell.top +
                $html_elements[$cp_graph[cell_id]].querySelector("#title")
                    .clientHeight +
                10;
            let left_pos = parent_cell.left + 25 + 12;
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
                let top_pos = prev_cell.top + prev_cell.height + 5;

                if ($cells[$id_map[cell_id]].top !== top_pos) {
                    $cells[$id_map[cell_id]].top = top_pos;
                }
                if ($cells[$id_map[cell_id]].left !== prev_cell.left) {
                    $cells[$id_map[cell_id]].left = prev_cell.left;
                }
            }
        }
    }
</script>

<div
    class="cell bg-white absolute w-fit h-fit dark:bg-vs-dark rounded-md border border-gray-500 dark:border-gray-400 shadow-md shadow-zinc-300 dark:shadow-neutral-900/50 flex overflow-visible cursor-default"
    bind:this={cell_div}
    style="
    top: {drag_cell_pos.y ? drag_cell_pos.y : $cells[$id_map[cell_id]].top}px;
    left: {drag_cell_pos.x ? drag_cell_pos.x : $cells[$id_map[cell_id]].left}px;
    z-index: {dragging ? 1000 : 0};
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
    <!-- <NewCellToolbar {cell_id} /> -->
</div>

<svelte:window on:mousemove={drag_mousemove} on:mouseup={drag_mouseup} />
