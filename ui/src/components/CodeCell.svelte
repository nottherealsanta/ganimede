<script lang="ts">
    import { onMount } from "svelte";
    import { id_map, cells } from "../stores/notebook";
    export let cell_id;
    $: cell = $cells[$id_map[cell_id]];

    // height and width
    let height = 0;
    let width = 0;
    $: cell.metadata.gm.height = height;
    $: cell.metadata.gm.width = width;
    onMount(() => {
        $cells[$id_map[cell_id]] = cell;
    });

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
        // cell.metadata.gm.top = Math.round(top / 12.5) * 12.5;
        // cell.metadata.gm.left = Math.round(left / 12.5) * 12.5;

        $cells[$id_map[cell_id]] = cell;
    };
    import { zoom } from "../stores/zoom";
    let mouseMove = function (event) {
        if (moving) {
            cell.metadata.gm.top = (event.pageY - clicked_y) / $zoom;
            cell.metadata.gm.left = (event.pageX - clicked_x) / $zoom;
            $cells[$id_map[cell_id]] = cell;
        }
    };

    // prime button
    const CellStates = {
        Idle: "idle",
        Queued: "queued",
        Running: "running",
        Done: "done",
    };
    let cell_state = CellStates.Idle;
    let run_promise;
    // let done = true;
    async function primary_button_click() {
        // done = false;
        cell_state = CellStates.Queued;
        $cells[$id_map[cell_id]]["outputs"] = [];
        async function running_promise() {
            console.log("runing : " + cell_id);
            const post_response = await fetch(`/notebook/run/${cell_id}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    code: cell.source.join("\n"),
                }),
            });
            const data = await post_response.json();
            cell_state = CellStates.Running;
            while (cell_state === CellStates.Running) {
                const get_response = await fetch(
                    `/notebook/output/${cell_id}`,
                    {
                        method: "GET",
                    }
                );
                const data = await get_response.json();
                if (data.execution_state === "idle") {
                    cell_state = CellStates.Done;
                }
                if (
                    data.output_type === "stream" ||
                    data.output_type === "display_data"
                ) {
                    $cells[$id_map[cell_id]]["outputs"] = [
                        ...$cells[$id_map[cell_id]]["outputs"],
                        data,
                    ];
                }
            }
        }
        run_promise = await running_promise();
        $cells[$id_map[cell_id]] = cell;
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
    active:border-gray-400 dark:active:border-neutral-800
    {focus ? 'border-sky-400' : 'border-gray-300 dark:border-vs-dark'}
    rounded-md
    absolute flex  justify-center overflow-visible 
    cursor-grab 
    active:cursor-grabbing
    w-fit
    min-h-[50px]"
    id="cell"
    on:mousedown={mouseDown}
    bind:clientHeight={height}
    bind:clientWidth={width}
>
    <div
        class="w-6 
        rounded-md
        flex flex-col 
        "
        id="sidebar"
    >
        <div
            class="h-6
            rounded-md
            flex justify-center items-center
            "
            id="primary-button"
            on:click={primary_button_click}
            on:keydown={primary_button_click}
            style="
            pointer-events: {cell_state === CellStates.Done ||
            cell_state === CellStates.Idle
                ? 'auto'
                : 'none'};
            "
        >
            <PrimeButton {cell_state} />
        </div>
    </div>
    <div class="w-auto h-full flex flex-col" id="not-sidebar">
        <CodeEditor {cell_id} bind:focus />
        {#if cell.outputs !== undefined}
            <Outputs {cell_id} />
        {/if}
    </div>
    <NewCellToolbar {cell_id} />
</div>

<svelte:window on:mouseup={mouseUp} on:mousemove={mouseMove} />
