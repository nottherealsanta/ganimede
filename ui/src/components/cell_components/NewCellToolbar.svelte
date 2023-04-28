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

    export let cell_id;

    // import { id_map, cells } from "../../stores/notebook";
    // $: cell = $cells[$id_map[cell_id]];

    function connector_click(e) {
        e.preventDefault();
        console.log("button click");
        console.log(e.target.id);
        e.stopPropagation();
    }

    let is_hover = false;

    import NewCellToolbarIcon from "./NewCellToolbarIcon.svelte";

    let item_class =
        "w-8 h-4 flex justify-center items-center -ml-0.25 hover:bg-neutral-100 dark:hover:bg-neutral-800 active:bg-neutral-200 dark:active:bg-neutral-700 ";
    let item_class_expect_first =
        "border-l border-gray-300 dark:border-neutral-700";

    import { send_message } from "../../stores/socket";

    async function new_code_cell() {
        send_message({
            channel: "notebook",
            method: "new_code_cell",
            message: {
                previous_cell_id: cell_id,
            },
        });
    }
</script>

<div
    class="absolute -bottom-0 left-0 w-full h-0 flex justify-center items-center"
>
    {#if is_hover}
        <div
            class="relative w-40 h-4 -bottom-0 flex flex-row justify-center items-center cursor-default
            bg-white dark:bg-vs-dark rounded border border-gray-300 dark:border-neutral-700
            overflow-clip fill-gray-600 dark:fill-gray-300 z-10"
            on:mouseleave={() => {
                is_hover = false;
                console.log("mouse out");
            }}
            on:blur={() => {
                // is_hover = false;
            }}
        >
            <div
                class={item_class}
                on:click={new_code_cell}
                on:keydown={() => {}}
            >
                <NewCellToolbarIcon icon_name="python" />
            </div>
            <div class={item_class + " " + item_class_expect_first}>
                <NewCellToolbarIcon icon_name="markdown" />
            </div>
            <div class={item_class + " " + item_class_expect_first}>
                <NewCellToolbarIcon icon_name="connector" />
            </div>
            <div class={item_class + " " + item_class_expect_first}>
                <NewCellToolbarIcon icon_name="disconnect" />
            </div>
            <div class={item_class + " " + item_class_expect_first}>
                <NewCellToolbarIcon icon_name="newCellMenu" />
            </div>
        </div>
    {:else}
        <div
            class="absolute w-2 h-2 rounded-full bg-transparent flex justify-center items-center
            cursor-pointer fill-neutral-400/75 dark:fill-neutral-300/75 stroke-neutral-400 dark:stroke-neutral-500 stroke-2"
            id="new-cell-toolbar"
            on:click|stopPropagation={connector_click}
            on:keydown={() => {}}
            on:mouseenter={() => {
                is_hover = true;
            }}
        >
            <svg
                class="w-full h-full pointer-events-none"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
            >
                <path
                    d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 100-12 6 6 0 000 12z"
                /></svg
            >
        </div>
    {/if}
</div>
