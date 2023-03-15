<script lang="ts">
    import CodeCell from "./CodeCell.svelte";
    import { onMount } from "svelte";
    import { id_map, cells } from "../stores/notebook";
    export let cell_id;
    $: cell = $cells[$id_map[cell_id]];

    // height and width
    let height = 0;
    let width = 0;
    // $: cell.metadata.gm.height = height;
    // $: cell.metadata.gm.width = width;
    $: if (cell) {
        cell.metadata.gm.height = height;
        cell.metadata.gm.width = width;
    }

    // draggability
    let top = 0;
    let left = 0;
    onMount(() => {
        top = cell.metadata.gm.top;
        left = cell.metadata.gm.left;
    });
    $: top = cell.metadata.gm.top;
    $: left = cell.metadata.gm.left;

    let moving = false;
    let clicked_x = 0;
    let clicked_y = 0;
    let mouseDown = function (event) {
        // if left click
        if (event.button === 0) {
            if (
                event.target.id === "cell" ||
                event.target.id === "sidebar" ||
                event.target.id === "not-sidebar"
            ) {
                moving = true;
                clicked_x = event.offsetX;
                clicked_y = event.offsetY;
            }
        }
    };
    let mouseUp = function () {
        moving = false;
        // snap to grid
        top = Math.round(top / 12.5) * 12.5;
        left = Math.round(left / 12.5) * 12.5;
    };
    import { zoom } from "../stores/zoom";
    let mouseMove = function (event) {
        if (moving) {
            cell.metadata.gm.top = (event.pageY - clicked_y) / $zoom;
            cell.metadata.gm.left = (event.pageX - clicked_x) / $zoom;
        }
    };

    import { Editor, rootCtx, defaultValueCtx } from "@milkdown/core";
    import { commonmark } from "@milkdown/preset-commonmark";

    function editor(dom) {
        Editor.make()
            .config((ctx) => {
                ctx.set(rootCtx, dom);
                ctx.set(defaultValueCtx, cell.source.join(""));
            })
            .use(commonmark)
            .create();
    }
</script>

<div
    style="
    top: {top}px; 
    left: {left}px;
    "
    class="cell"
    id="cell"
    on:mousedown|self={mouseDown}
>
    <div class="sidebar" id="sidebar">
        <div class="collapse-button" />
    </div>
    <div class="not-sidebar" id="not-sidebar">
        <div use:editor class="md-editor" />
    </div>
</div>
<div class="children" style="top: {top + 25}px; left: {left}px;">
    {#each cell.metadata.gm.children as child_id}
        {#if $cells[$id_map[child_id]].cell_type === "code"}
            <CodeCell cell_id={child_id} />
        {/if}
        {#if $cells[$id_map[child_id]].cell_type === "markdown"}
            <svelte:self cell_id={child_id} />
        {/if}
    {/each}
</div>

<svelte:window on:mouseup={mouseUp} on:mousemove={mouseMove} />

<style>
    .cell {
        top: 100px;
        left: 100px;

        background-color: rgba(230, 230, 230, 0.455);
        box-shadow: rgba(17, 17, 26, 0.1) 0px 3px 12px,
            rgba(17, 17, 26, 0.05) 0px 6px 24px;
        border: solid 1px rgb(170, 170, 170);
        border-radius: 6px;
        position: absolute;
        display: flex;
        padding: 5px 0px 5px 2px;

        cursor: grab;

        width: fit-content;
        height: fit-content;

        min-width: 300px;
        min-height: 25px;
    }
    .cell:hover {
        border: solid 1px #c7c7c7;
    }
    .cell:active {
        border: solid 1px #b7b7b7;
        cursor: grabbing;
    }
    .sidebar {
        width: 25px;
        border-radius: 5px;
        float: left;
        flex-direction: column;
        padding-top: 2px;
        padding-right: 2px;
    }

    .not-sidebar {
        width: auto;
        height: 100%;
        float: right;
        display: flex;
        flex-direction: column;
        margin-left: 0px;

        align-items: middle;
    }

    .md-editor {
        height: fit-content;
        width: fit-content;
        min-width: 200px;
        margin: 5px 0px 5px 0px;
    }

    .children {
        width: 100px;
        height: max-content;
        display: flex;
        flex-direction: column;
        margin-left: 0px;
        background-color: aliceblue;
        position: absolute;
    }

    /* dark mode */
    @media (prefers-color-scheme: dark) {
        .cell {
            background-color: rgba(30, 30, 30, 0.726);
            border: solid 1px #2a2a2a;
            box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px,
                rgba(17, 17, 26, 0.05) 0px 8px 32px;
        }
        .cell:hover {
            border: solid 1px #3a3a3a;
        }
        .cell:active {
            border: solid 1px #4a4a4a;
            z-index: 1;
        }
    }
</style>
