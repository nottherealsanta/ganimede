<script lang="ts">
    // import { stop_propagation } from "svelte/internal";
    // import { notebook, cells, id_map } from "../../stores/notebook";
    // import { send_message } from "../../stores/socket";
    // // export let cell_id;

    // async function new_code_cell() {
    //     send_message({
    //         channel: "notebook",
    //         method: "new_code_cell",
    //         message: {
    //             previous_cell_id: "asd", //cell_id,
    //         },
    //     });
    // }

    // function new_text_cell() {
    //     console.log("new text cell");
    // }

    function connector_click(e) {
        e.preventDefault();
        console.log("button click");
        console.log(e.target.id);
        e.stopPropagation();
    }

    let is_hover = false;

    import NewCellToolbarIcon from "./NewCellToolbarIcon.svelte";
</script>

<div
    class="absolute -bottom-0 left-0 w-full h-0 flex justify-center items-center pointer-events-auto"
    on:mouseleave={() => {
        is_hover = false;
    }}
>
    {#if is_hover}
        <div
            class="relative w-40 h-4 flex flex-row justify-center items-center cursor-default bg-white dark:bg-vs-dark rounded border border-gray-300 dark:border-neutral-700 overflow-clip"
        >
            <div class="w-8 h-4 flex justify-center items-center -ml-0.25">
                <NewCellToolbarIcon icon_name="python" />
            </div>
            <div
                class="w-8 h-4 flex justify-center items-center -ml-0.25 border-l border-gray-300 dark:border-neutral-700"
            >
                <NewCellToolbarIcon icon_name="markdown" />
            </div>
            <div
                class="w-8 h-4 flex justify-center items-center -ml-0.25 border-l border-gray-300 dark:border-neutral-700"
            >
                <NewCellToolbarIcon icon_name="connector" />
            </div>
            <div
                class="w-8 h-4 flex justify-center items-center -ml-0.25 border-l border-gray-300 dark:border-neutral-700"
            >
                <div>p</div>
            </div>
            <div
                class="w-8 h-4 flex justify-center items-center -ml-0.25 border-l border-gray-300 dark:border-neutral-700"
            >
                <div>p</div>
            </div>
        </div>
    {:else}
        <div
            class="absolute w-2 h-2 hover:w-2.5 hover:h-2.5 rounded-full bg-gray-300/40 hover:bg-gray-100 flex justify-center items-center cursor-pointer"
            id="new-cell-toolbar"
            on:click|stopPropagation={connector_click}
            on:keydown={() => {}}
            on:mouseenter={() => {
                is_hover = true;
            }}
        >
            <svg
                class="w-full h-full pointer-events-none text-white dark:text-gray-800"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
            >
                <path
                    fill-rule="evenodd"
                    d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 100-12 6 6 0 000 12z"
                    clip-rule="evenodd"
                /></svg
            >
        </div>
    {/if}
</div>
