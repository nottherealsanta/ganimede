<script>
    export let cell_id;

    import { id_map, cells } from "../../stores/notebook";
    $: cell = $cells[$id_map[cell_id]];

    let hover = false;
    let div = null;
    // run
    import { send_message } from "../../stores/socket";
    const CellStates = {
        Idle: "idle",
        Queued: "queued",
        Running: "running",
        Done: "done",
    };
    let cell_state = CellStates.Idle;
    async function primary_button_click() {
        div.disabled = true;
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
            div.disabled = false;
        }, 1000);
    }
</script>

<div
    class="bg-transparent hover:bg-neutral-100 dark:hover:bg-neutral-800 active:bg-neutral-200 dark:active:bg-neutral-700
    flex w-6 h-6 p-0 m-0 border border-zinc-100 dark:border-neutral-800 rounded items-center justify-center mr-1"
    on:click={(e) => {
        e.stopPropagation();
        primary_button_click();
    }}
    on:keydown={() => {}}
    on:mouseenter={() => {
        hover = true;
    }}
    on:mouseleave={() => {
        hover = false;
    }}
    bind:this={div}
>
    {#if hover}
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
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
    {:else}
        <div class="font-mono text-[11px]">{cell.execution_count}</div>
    {/if}
</div>

<style>
    .run-button-svg {
        color: #000000;
        margin: 0 auto;
        display: block;
    }
    /* dark mode */
    @media (prefers-color-scheme: dark) {
        .run-button-svg {
            color: rgba(209, 209, 209, 1);
        }
    }
</style>
