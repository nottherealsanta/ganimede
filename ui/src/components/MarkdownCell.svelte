<script lang="ts">
    import { onMount } from "svelte";
    import { id_map, cells } from "../stores/notebook";
    export let cell_id;
    $: cell = $cells[$id_map[cell_id]];

    // height and width
    let height = 0;
    let width = 0;
    // $: cell.height = height;
    // $: cell.width = width;
    $: if (cell) {
        cell.height = height;
        cell.width = width;
    }
    onMount(() => {
        $cells[$id_map[cell_id]] = cell;
    });

    // draggability
    let top = 0;
    let left = 0;
    onMount(() => {
        top = cell.top;
        left = cell.left;
    });
    $: top = cell.top;
    $: left = cell.left;

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
        // top = Math.round(top / 12.5) * 12.5;
        // left = Math.round(left / 12.5) * 12.5;

        $cells[$id_map[cell_id]] = cell;
    };
    import { zoom } from "../stores/zoom";
    let mouseMove = function (event) {
        if (moving) {
            cell.top = (event.pageY - clicked_y) / $zoom;
            cell.left = (event.pageX - clicked_x) / $zoom;
            $cells[$id_map[cell_id]] = cell;
        }
    };

    import { Editor, rootCtx, defaultValueCtx } from "@milkdown/core";
    import { commonmark } from "@milkdown/preset-commonmark";
    import { children } from "svelte/internal";

    function editor(dom) {
        Editor.make()
            .config((ctx) => {
                ctx.set(rootCtx, dom);
                ctx.set(defaultValueCtx, cell.source.join("\n"));
            })
            .use(commonmark)
            .create();
    }

    // children height and width
    // let tissue_height = 0;
    // let tissue_width = 0;
    // onMount(() => {
    //     let children = cell.children;
    //     for (let i = 0; i < children.length; i++) {
    //         console.log("children[i]", children[i]);
    //         tissue_height += $cells[$id_map[children[i]]].height;
    //         tissue_width += $cells[$id_map[children[i]]].width;
    //     }
    //     console.log("tissue_height", tissue_height);
    //     console.log("tissue_width", tissue_width);
    // });
</script>

<div
    style="
    top: {top}px; 
    left: {left}px;
    "
    class="
    bg-neutral-200/70 dark:bg-neutral-700/40
    p-0.5
    rounded-md
    shadow-md shadow-zinc-300 dark:shadow-neutral-900/50
    border border-gray-300 dark:border-gray-700
    hover:border-gray-400 dark:hover:border-gray-600
    active:border-gray-500 dark:active:border-gray-500
    w-fit
    h-fit
    cursor-grab
    absolute
    flex
    flex-col
    justify-center
    resize
    min-w-300
    overflow-visible
    "
    id="cell"
    on:mousedown={mouseDown}
    bind:clientHeight={height}
    bind:clientWidth={width}
>
    <div class="flex flex-row">
        <div class="w-6 rounded-md flex flex-col" id="sidebar">
            <div class="collapse-button" />
        </div>
        <div
            class="w-auto h-full flex flex-col pt-1 pb-1 pr-1"
            id="not-sidebar"
        >
            <div
                use:editor
                class="bg-gray-50/100 dark:bg-neutral-800/100 w-full h-fit mr-10 rounded-sm"
            />
        </div>
    </div>
    <div class="bg-red-500 rounded-md bottom-0 w-full h-full" />
</div>

<svelte:window on:mouseup={mouseUp} on:mousemove={mouseMove} />
