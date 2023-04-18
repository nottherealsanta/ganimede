<!-- <script lang="ts">
    import { onMount } from "svelte";
    import { id_map, cells } from "../stores/notebook";
    export let cell_id;
    $: cell = $cells[$id_map[cell_id]];

    // height and width
    let height = 0;
    let width = 0;
    $: cell.height = height;
    $: cell.width = width;
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
        // cell.top = Math.round(top / 12.5) * 12.5;
        // cell.left = Math.round(left / 12.5) * 12.5;

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

    // prime button
    import { send_message } from "../stores/socket";
    const CellStates = {
        Idle: "idle",
        Queued: "queued",
        Running: "running",
        Done: "done",
    };
    let primary_button;
    let cell_state = CellStates.Idle;
    async function primary_button_click() {
        cell_state = CellStates.Queued;
        $cells[$id_map[cell_id]]["outputs"] = [];
        console.log("sending message");
        send_message({
            channel: "notebook",
            method: "run",
            message: {
                cell_id: cell_id,
                code: cell.source,
            },
        });

        $cells[$id_map[cell_id]] = cell;

        // disable button for 1 second
        // disable max (500ms, cell_state === "running")
        // disable till resposse of state
        setTimeout(() => {
            primary_button.disabled = false;
        }, 1000);
    }

    // CodeEditor
    import CodeEditor from "./cell_components/CodeEditor.svelte";
    let focus;

    // Outputs
    import Outputs from "./cell_components/Outputs.svelte";

    //Sidebar
    import PrimeButton from "./cell_components/PrimeButton.svelte";

    //NewCellToolbar
    import NewCellToolbar from "./cell_components/NewCellToolbar.svelte";

    // transitions
    import { fade } from "svelte/transition";

    let cell_div;
</script>

<div
    style="
    top: {top}px; 
    left: {left}px;
    "
    class="
    bg-white dark:bg-vs-dark
    p-0.5
    shadow-md shadow-zinc-300 dark:shadow-neutral-900/50
    border
    border-gray-300 dark:border-neutral-800
    active:border-gray-400 dark:active:border-neutral-800
    {focus ? 'border-sky-400' : 'border-gray-300 dark:border-vs-dark'}
    rounded-md
    absolute flex justify-center overflow-visible
    cursor-grab
    active:cursor-grabbing
    w-fit
    min-h-[30px]"
    id="cell"
    on:mousedown={mouseDown}
    bind:clientHeight={height}
    bind:clientWidth={width}
    transition:fade={{ duration: 100 }}
    bind:this={cell_div}
>
    <div
        class="w-6
        rounded-md
        flex flex-col
        "
        id="sidebar"
    >
        <button
            class="h-6
            rounded-md
            flex justify-center items-center
            cursor-pointer
            border border-transparent
            hover:bg-gray-200 dark:hover:bg-neutral-800
            active:bg-gray-300 dark:active:bg-neutral-700
            focus:outline-none
            disabled:bg-gray-100 dark:disabled:bg-neutral-900
            "
            id="primary-button"
            on:click={primary_button_click}
            on:keydown={primary_button_click}
            bind:this={primary_button}
        >
            <PrimeButton {cell_state} />
        </button>
    </div>
    <div class="w-auto h-full flex flex-col" id="not-sidebar">
        <CodeEditor {cell_id} bind:focus />
        {#if cell.outputs.length > 0}
            <Outputs {cell_id} />
        {/if}
    </div>

    <NewCellToolbar {cell_id} />
</div>

<svelte:window on:mouseup={mouseUp} on:mousemove={mouseMove} /> -->

<script lang="ts">
    import Cell from "./Cell.svelte";
    import { id_map, cells } from "../stores/notebook";
    import Outputs from "./cell_components/Outputs.svelte";

    export let cell_id;

    $: cell = $cells[$id_map[cell_id]];

    import CodeEditor from "./cell_components/CodeEditor.svelte";
    import { onMount } from "svelte";
    let focus;
</script>

<Cell {cell}>
    <!-- <div class="w-6rounded-md flex flex-col">
        <button id="primary-button">a </button>
    </div>--
    <div class="w-auto h-full flex flex-col"> -->
    <CodeEditor {cell_id} bind:focus />
    {#if cell.outputs.length > 0}
        <Outputs {cell_id} />
    {/if}

    <!-- </div> -->
    <!-- </div> -->
</Cell>
