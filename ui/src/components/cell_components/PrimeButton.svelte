<script>
    export let cell_id;

    import { id_map, cells, notebook } from "../../stores/notebook";
    $: cell = $cells[$id_map[cell_id]];

    let hover = false;
    // let execution_count;
    // $: if (cell) {
    //     if (cell.execution_count === null) {
    //         execution_count = "[ ]";
    //     } else {
    //         execution_count = cell.execution_count;
    //     }
    // }

    let div = null;
    // run
    import { send_message } from "../../stores/socket";
    async function primary_button_click() {
        let state = $cells[$id_map[cell_id]].state;
        if (state === "idle") {
            send_message({
                channel: "notebook",
                method: "queue_cell",
                message: {
                    cell_id: cell_id,
                    code: cell.source,
                },
            });
        }
        if (state === "queued" || state === "running") {
            send_message({
                channel: "notebook",
                method: "interrupt_kernel",
                message: {},
            });
        }
    }
</script>

<div
    class="flex flex-none bg-transparent hover:bg-oli-100 dark:hover:bg-oli-800 active:bg-oli-200 dark:active:bg-oli-700 w-5 h-5 p-0 m-0 rounded-sm items-center justify-center stroke-black dark:stroke-white fill-black dark:fill-white cursor-pointer pointer-events-auto"
    on:mousedown|stopPropagation={(e) => {
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
    {#if $cells[$id_map[cell_id]].state == "idle"}
        <!-- {#if hover} -->
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
        >
            <polygon points="19 12 19 43 43 27.5 19 12" />
        </svg>
        <!-- {:else}
            <div class="font-mono text-[11px]">{execution_count}</div>
        {/if} -->
    {:else if $cells[$id_map[cell_id]].state == "queued"}
        {#if hover}
            <svg
                viewBox="0 0 20 20"
                fill="currentColor"
                xmlns="http://www.w3.org/2000/svg"
                stroke="currentColor"
                stroke-width="0.5"
            >
                <rect x="6" y="6" width="7" height="7" />
            </svg>
        {:else}
            <svg
                version="1.1"
                id="L9"
                xmlns="http://www.w3.org/2000/svg"
                x="0px"
                y="0px"
                viewBox="0 0 100 100"
                enable-background="new 0 0 0 0"
            >
                <path
                    d="M73,50c0-12.7-10.3-23-23-23S27,37.3,27,50 M30.9,50c0-10.5,8.5-19.1,19.1-19.1S69.1,39.5,69.1,50"
                >
                    <animateTransform
                        attributeName="transform"
                        type="rotate"
                        dur="5s"
                        from="360 50 50"
                        to="0 50 50"
                        repeatCount="indefinite"
                    />
                </path>
            </svg>
        {/if}
    {:else if $cells[$id_map[cell_id]].state == "running"}
        {#if hover}
            <svg
                viewBox="0 0 20 20"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                stroke="currentColor"
                stroke-width="0.5"
            >
                <rect x="6" y="6" width="7" height="7" />
            </svg>
        {:else}
            <svg
                version="1.1"
                id="L9"
                xmlns="http://www.w3.org/2000/svg"
                x="0px"
                y="0px"
                viewBox="0 0 100 100"
                enable-background="new 0 0 0 0"
            >
                <path
                    d="M73,50c0-12.7-10.3-23-23-23S27,37.3,27,50 M30.9,50c0-10.5,8.5-19.1,19.1-19.1S69.1,39.5,69.1,50"
                >
                    <animateTransform
                        attributeName="transform"
                        type="rotate"
                        dur="1s"
                        from="0 50 50"
                        to="360 50 50"
                        repeatCount="indefinite"
                    />
                </path>
            </svg>
        {/if}
    {/if}
</div>
