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

    // run cell
    let run_promise;
    let done = true;
    async function run() {
        done = false;
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
            let done = true;
            while (done) {
                const get_response = await fetch(
                    `/notebook/output/${cell_id}`,
                    {
                        method: "GET",
                    }
                );
                const data = await get_response.json();
                if (data.execution_state === "idle") {
                    done = false;
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
                // console.log(data);
            }
        }
        run_promise = await running_promise();
        done = true;
    }

    // CodeEditor
    import CodeEditor from "./cell_components/CodeEditor.svelte";
    let focus;

    // Outputs
    import Outputs from "./cell_components/Outputs.svelte";
</script>

<div
    style="
    top: {top}px; 
    left: {left}px;
    border: {focus ? 'solid 1px rgb(1,1,1, 0.5)' : 'solid 1px rgb(1,1,1, 0.1)'};
    "
    class="cell"
    id="cell"
    on:mousedown={mouseDown}
    bind:clientHeight={height}
    bind:clientWidth={width}
>
    <div class="sidebar" id="sidebar">
        <div class="run-button" on:click={run} on:keydown={run}>
            {#if !done}
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
            {:else}
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
            {/if}
        </div>
    </div>
    <div class="not-sidebar" id="not-sidebar">
        <CodeEditor {cell_id} bind:focus />
        <Outputs {cell_id} />
    </div>
    <div class="resize-bar" />
</div>

<svelte:window on:mouseup={mouseUp} on:mousemove={mouseMove} />

<style>
    .cell {
        top: 100px;
        left: 100px;

        background-color: #ffffff;
        box-shadow: rgba(17, 17, 26, 0.1) 0px 3px 12px,
            rgba(17, 17, 26, 0.05) 0px 6px 24px;
        border: solid 1px #3583dc;
        border-radius: 8px;
        position: absolute;
        display: flex;
        padding: 3px 0px 3px 0px;

        /* cursor: grab; */

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
        .cell:hover {
            border: solid 1px #3a3a3a;
        }
        .cell:active {
            border: solid 1px #4a4a4a;
            z-index: 1;
        }

        .run-button-svg {
            color: rgba(103, 154, 209, 1);
        }
    }
</style>
