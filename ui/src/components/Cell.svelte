<script lang="ts">
    import { onMount } from "svelte";
    import { notebook, id_map } from "../stores/notebook";
    export let cell_id;
    $: cell = $notebook["cells"][$id_map[cell_id]];

    // height and width
    let height = 0;
    let width = 0;
    $: cell.metadata.gm.height = height;
    $: cell.metadata.gm.width = width;

    // draggability
    let top = 0;
    let left = 0;
    onMount(() => {
        top = cell.metadata.gm.top;
        left = cell.metadata.gm.left;
    });
    $: cell.metadata.gm.top = top;
    $: cell.metadata.gm.left = left;

    let moving = false;
    let clicked_x = 0;
    let clicked_y = 0;
    let mouseDown = function (event) {
        if (
            event.target.id === "cell" ||
            event.target.id === "sidebar" ||
            event.target.id === "not-sidebar"
        ) {
            moving = true;
            clicked_x = event.offsetX;
            clicked_y = event.offsetY;
        }
    };
    let mouseUp = function () {
        moving = false;
        // snap to grid 25
        top = Math.round(top / 25) * 25;
        left = Math.round(left / 25) * 25;
    };
    import { zoom } from "../stores/zoom";
    let mouseMove = function (event) {
        if (moving) {
            top = (event.pageY - clicked_y) / $zoom;
            left = (event.pageX - clicked_x) / $zoom;
        }
    };

    // run cell
    async function run() {
        console.log("run");
        console.log(cell);
        const post_response = await fetch(`/notebook/run/${cell_id}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                code: cell.source.join("\n"),
            }),
        });
        // await post_response;
        let done = true;
        while (done) {
            const get_response = await fetch(`/notebook/output/${cell_id}`, {
                method: "GET",
            });
            const data = await get_response.json();
            if (data.execution_state === "idle") {
                done = false;
            }
            if (data.output_type === "stream") {
                $notebook["cells"][$id_map[cell_id]]["outputs"][0].text =
                    data.text;
            }
            console.log(data);
        }
        console.log("done");
    }

    let run_promise;

    async function run_click() {
        run_promise = run();
    }

    // CodeEditor
    import CodeEditor from "./cell_components/CodeEditor.svelte";

    // Outputs
    import Outputs from "./cell_components/Outputs.svelte";
</script>

<div
    style="
    top: {top}px; 
    left: {left}px;
    "
    class="cell"
    id="cell"
    on:mousedown={mouseDown}
    bind:clientHeight={height}
    bind:clientWidth={width}
>
    <div class="sidebar" id="sidebar">
        <div class="run-button" on:click={run_click} on:keydown={run_click}>
            {#await run_promise}
                <!-- animate svg loading circle -->
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 55 55"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="run-button-svg"
                >
                    <circle cx="27.5" cy="27.5" r="25" />
                </svg>
            {:then d}
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 55 55"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="run-button-svg"
                >
                    <polygon points="19 12 19 43 43 27.5 19 12" />
                </svg>
            {/await}
        </div>
    </div>
    <div class="not-sidebar" id="not-sidebar">
        <CodeEditor {cell_id} />
        <Outputs {cell_id} />
    </div>
    <div class="resize-bar" />
</div>

<svelte:window on:mouseup={mouseUp} on:mousemove={mouseMove} />

<style>
    .cell {
        top: 100px;
        left: 100px;

        background-color: #f7f7f7;
        box-shadow: rgba(17, 17, 26, 0.1) 0px 3px 12px,
            rgba(17, 17, 26, 0.05) 0px 6px 24px;
        border: solid 1px #d7d7d7;
        border-radius: 10px;
        position: absolute;
        display: flex;
        padding: 5px 0px 5px 2px;

        cursor: grab;

        min-width: 300px;
        min-height: 25px;
    }
    .sidebar {
        width: 25px;
        border-radius: 5px;
        float: left;
        flex-direction: column;
        padding-top: 2px;
        padding-right: 2px;
    }
    .run-button {
        width: 100%;
        height: 25px;
        background-color: rgba(255, 255, 255, 0);
        border-radius: 5px;
        cursor: default;
        display: flex;
        align-items: center;
    }
    .run-button:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }
    .run-button:active {
        background-color: rgba(0, 0, 0, 0.2);
    }
    .run-button-svg {
        color: #000000;
        margin: 0 auto;
        display: block;
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
    .resize-bar {
        width: 5px;
        height: 90%;
        background-color: rgba(215, 215, 215, 0);
        border-radius: 5px;
        float: bottom;
        transition: 0.3s;
        align-self: center;
    }

    .resize-bar:hover {
        width: 5px;
        background-color: rgba(138, 138, 138, 0.455);
        cursor: ew-resize;
    }

    /* dark mode */
    @media (prefers-color-scheme: dark) {
        .cell {
            background-color: #242424;
            border: solid 1px #2a2a2a;
            box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px,
                rgba(17, 17, 26, 0.05) 0px 8px 32px;
        }

        .run-button-svg {
            color: rgba(103, 154, 209, 1);
        }
    }
</style>
