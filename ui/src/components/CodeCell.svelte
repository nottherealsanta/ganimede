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
        cell.metadata.gm.top = Math.round(top / 12.5) * 12.5;
        cell.metadata.gm.left = Math.round(left / 12.5) * 12.5;

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

<!-- if focus variable is true, then cell:focus -->
<div
    style="
    top: {top}px; 
    left: {left}px;
    "
    class:focus
    class="cell"
    id="cell"
    on:mousedown={mouseDown}
    bind:clientHeight={height}
    bind:clientWidth={width}
>
    <div class="sidebar" id="sidebar">
        <div
            class="primary-button"
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
    <div class="not-sidebar" id="not-sidebar">
        <CodeEditor {cell_id} bind:focus />
        {#if cell.outputs !== undefined}
            <Outputs {cell_id} />
        {/if}
    </div>
    <NewCellToolbar {cell_id} />
</div>

<svelte:window on:mouseup={mouseUp} on:mousemove={mouseMove} />

<style>
    .cell {
        top: 100px;
        left: 100px;

        background-color: #ffffff;
        box-shadow: rgba(17, 17, 26, 0.1) 0px 3px 12px,
            rgba(17, 17, 26, 0.05) 0px 6px 24px;
        border: solid 1px #d8d8d8;
        border-radius: 8px;
        position: absolute;
        display: flex;
        padding: 1px 3px 3px 3px;
        justify-content: center;
        overflow: visible;

        cursor: grab;

        min-width: 300px;
        min-height: 50px;
    }
    .cell:active {
        border: solid 1px #b7b7b7;
        cursor: grabbing;
    }
    .focus {
        border: solid 1px #000000;
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

    .sidebar {
        width: 25px;
        border-radius: 5px;
        float: left;
        flex-direction: column;
        padding-top: 2px;
        padding-right: 2px;
    }
    .primary-button {
        width: 100%;
        height: 25px;
        background-color: rgba(255, 255, 255, 0);
        border-radius: 5px;
        cursor: default;
        display: flex;
        align-items: center;
    }
    .primary-button:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }
    .primary-button:active {
        background-color: rgba(0, 0, 0, 0.2);
    }

    /* dark mode */
    @media (prefers-color-scheme: dark) {
        .cell {
            background-color: rgb(30, 30, 30);
            border: solid 1px #2a2a2a;
            box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px,
                rgba(17, 17, 26, 0.05) 0px 8px 32px;
        }
        .cell:active {
            border: solid 1px #b0b0b0;
            z-index: 1;
        }
        .focus {
            border: solid 1px #1075b8;
            box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px,
                rgba(17, 17, 26, 0.05) 0px 8px 32px;
        }
    }
</style>
