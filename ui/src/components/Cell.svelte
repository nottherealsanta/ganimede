<script lang="ts">
    import { onMount } from "svelte";
    import { notebook, id_map } from "../stores/notebook";
    export let cell_id;
    $: cell = $notebook["cells"][$id_map[cell_id]];

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
        // route "/notebook/run/{cell_id}",
        const response = await fetch(`/notebook/run/${cell_id}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                code: code,
            }),
        });
        const data = await response.json();
        console.log(data);
    }

    // CodeEditor
    import CodeEditor from "./cell_components/CodeEditor.svelte";

    $: code = cell.source.join("");

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
>
    <div class="sidebar" id="sidebar">
        <div class="run-button" on:click={run} on:keydown={run}>
            <!-- svg for play button -->
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="25"
                height="25"
                viewBox="0 0 55 55"
                fill="none"
                stroke="currentColor"
                stroke-width="3"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="run-button-svg"
            >
                <!-- <polygon points="17 12 17 38 38 25 17 12" /> -->
                <polygon points="19 12 19 43 43 27.5 19 12" />
            </svg>
        </div>
    </div>
    <div class="not-sidebar" id="not-sidebar">
        <CodeEditor bind:code />
        <!-- <div class="outputs" /> -->
        <Outputs />
    </div>
    <div class="resize-bar" />
</div>

<svelte:window on:mouseup={mouseUp} on:mousemove={mouseMove} />

<style>
    .cell {
        top: 100px;
        left: 100px;

        background-color: #f5f5f5;
        box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px,
            rgba(17, 17, 26, 0.05) 0px 8px 32px;
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
        float: top;
        cursor: default;
    }
    .run-button:hover {
        background-color: rgba(0, 0, 0, 0.1);
    }
    .run-button-svg {
        color: #000000;
    }

    .not-sidebar {
        width: 100%;
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
            background-color: #1e1e1e;
            border: solid 1px #2a2a2a;
            box-shadow: rgba(17, 17, 26, 0.1) 0px 4px 16px,
                rgba(17, 17, 26, 0.05) 0px 8px 32px;
        }

        .run-button-svg {
            color: rgba(103, 154, 209, 1);
        }
    }
</style>
