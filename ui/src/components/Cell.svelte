<script lang="ts">
    // draggable
    let moving = false;
    let top = 0;
    let left = 0;

    function mouseDown(event) {
        if (
            event.target.id === "cell" ||
            event.target.id === "sidebar" ||
            event.target.id === "not-sidebar"
        ) {
            moving = true;
        }
    }
    function mouseUp() {
        moving = false;
    }
    function mouseMove(e) {
        if (moving) {
            top += e.movementY;
            left += e.movementX;
        }
    }

    // run cell
    function run() {
        console.log("run");
    }

    // CodeEditor
    import CodeEditor from "./cell_components/CodeEditor.svelte";

    let code = "print('hello world')";
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
                viewBox="0 0 50 50"
                fill="none"
                stroke="currentColor"
                stroke-width="3"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="feather feather-play"
            >
                <polygon points="17 12 17 38 38 25 17 12" />
            </svg>
        </div>
    </div>
    <div class="not-sidebar" id="not-sidebar">
        <CodeEditor bind:code />
        <!-- <div class="outputs" /> -->
    </div>
    <div class="resize-bar" />
</div>

<svelte:window on:mouseup={mouseUp} on:mousemove={mouseMove} />

<style>
    .cell {
        top: 100px;
        left: 100px;

        background-color: #f5f5f5;
        box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
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
    }
    .run-button {
        width: 100%;
        height: 25px;
        background-color: rgba(255, 255, 255, 0);
        border-radius: 5px;
        float: top;
        cursor: default;
    }
    .not-sidebar {
        width: 100%;
        height: 100%;
        float: right;
        display: flex;
        flex-direction: column;
        margin-left: 5px;

        align-items: middle;
    }

    .outputs {
        width: 100%;
        height: 100%;
        background-color: #c28181;
        border-radius: 5px;
        float: bottom;
        margin-top: 5px;
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
            box-shadow: 0 0 10px 0 rgba(213, 213, 213, 0.2);
        }
        .outputs {
            background-color: #5866a2;
        }
    }
</style>
