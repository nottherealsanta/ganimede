<script>
    import CodeCell from "./CodeCell.svelte";
    import MarkdownCell from "./MarkdownCell.svelte";
    import Edges from "./utility_components/Edges.svelte";

    import {
        notebook,
        cells,
        id_map,
        np_graph,
        pc_graph,
        heading_levels_inv,
        parent_less_cells,
    } from "../stores/notebook";

    setTimeout(() => {
        if (window.scrollX === 0 && window.scrollY === 0) {
            window.scrollTo(5000 - 400, 1000 - 200);
        }
    }, 1500);

    import DragSelect from "dragselect";
    import { onMount } from "svelte";

    let ds = null;

    onMount(() => {
        setTimeout(() => {
            ds = new DragSelect({
                selectables: document.getElementsByClassName("cell"),
                useTransform: false,
                dragAsBlock: true,
                // area: document.getElementById("canvas"),
            });
            ds.subscribe("dragmove", (callback_object) => {
                if (callback_object.items.length > 0) {
                    for (let item of callback_object.items) {
                        let cell_id = item.getAttribute("cell_id");
                        let top = item.style.top;
                        let left = item.style.left;
                        $cells[$id_map[cell_id]].top = parseInt(top);
                        $cells[$id_map[cell_id]].left = parseInt(left);
                    }
                }
            });
            ds.subscribe("callback", (dropTarget) => {
                console.log("Callback", dropTarget);
                if (dropTarget?.itemsDropped?.length) {
                    console.log(
                        "Dropped",
                        dropTarget.itemsDropped,
                        "into",
                        dropTarget.id
                    );
                }
            });
        }, 1000);
    });
</script>

<div class="notebook">
    {#if Object.keys($notebook).length !== 0}
        {#each [1, 2, 3, 4, 5, 6] as level}
            {#each $heading_levels_inv[level] as cell_id}
                {#if $cells[$id_map[cell_id]].type === "markdown"}
                    <MarkdownCell {cell_id} />
                {/if}
                {#if $pc_graph[cell_id]}
                    {#each $pc_graph[cell_id] as child_id}
                        {#if $cells[$id_map[child_id]].type === "markdown" && !(child_id in $pc_graph)}
                            <MarkdownCell cell_id={child_id} />
                        {/if}
                        {#if $cells[$id_map[child_id]].type === "code"}
                            <CodeCell cell_id={child_id} />
                        {/if}
                        {#if $np_graph[child_id]}
                            {#each $np_graph[child_id] as next_id}
                                <Edges current_cell_id={child_id} {next_id} />
                            {/each}
                        {/if}
                    {/each}
                {/if}

                {#if $np_graph[cell_id]}
                    {#each $np_graph[cell_id] as next_id}
                        <Edges current_cell_id={cell_id} {next_id} />
                    {/each}
                {/if}
            {/each}
        {/each}

        {#each $parent_less_cells as cell_id}
            {#if $cells[$id_map[cell_id]].type === "markdown"}
                <MarkdownCell {cell_id} />
            {/if}
            {#if $cells[$id_map[cell_id]].type === "code"}
                <CodeCell {cell_id} />
            {/if}
            {#if $np_graph[cell_id]}
                {#each $np_graph[cell_id] as next_id}
                    <Edges current_cell_id={cell_id} {next_id} />
                {/each}
            {/if}
        {/each}
    {/if}
</div>

<style>
    .notebook {
        display: flex;
        flex-direction: column;
    }
</style>
