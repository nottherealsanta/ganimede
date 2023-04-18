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

    function middle_button_click(e) {
        e.preventDefault();
        console.log("button click");
        console.log(e.target.id);
        e.stopPropagation();
    }

    let is_hover = false;

    let tools = ["python", "markdown", "disconnect"];
</script>

<!-- <style>
    .new-cell-toolbar {
        position: absolute;
        bottom: -4px;
        background-color: transparent;
        width: 90%;
        align-content: center;
        justify-content: center;
        height: 6px;
        cursor: default;
        display: flex;
        overflow: hidden;
    }
    .new-cell-toolbar:hover {
        height: 8px;
        background-color: transparent;
        overflow: visible;
    }

    .new-cell-button {
        width: 40px;
        height: fit-content;
        background-color: #ffffff;
        color: #383838;
        cursor: pointer;
        padding: 0%;
        margin: 0px 5px 0px 5px;
        top: -4px;
        position: relative;
        font-size: x-small;
        border-radius: 2px;
        font-family: Verdana, Geneva, Tahoma, sans-serif;
    }
    .new-cell-toolbar .new-cell-button {
        visibility: hidden;
        z-index: -1;
    }
    .new-cell-toolbar:hover .new-cell-button {
        visibility: visible;
        background-color: #cdcdcd;
        z-index: 99;
    }

    /* dark mode */
    @media (prefers-color-scheme: dark) {
        .new-cell-button {
            border: solid 1px #3f3f3f;
            color: #cdcdcd;
        }
        .new-cell-toolbar:hover .new-cell-button {
            background-color: #2b2b2b;
        }
    }
</style> -->

<!-- on click console log -->
<div
    class="absolute -bottom-0 left-0 w-full h-0 flex justify-center items-center pointer-events-auto"
>
    <div
        class="relative w-2 h-2 hover:w-3 hover:h-3 rounded-full bg-gray-300/40 hover:bg-gray-100 flex justify-center items-center cursor-pointer"
        id="new-cell-toolbar"
        on:click|stopPropagation={middle_button_click}
        on:keydown={() => {}}
        on:mouseenter={() => {
            is_hover = true;
        }}
    >
        <svg
            class="w-full h-full pointer-events-none"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
        >
            <path
                fill-rule="evenodd"
                d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 100-12 6 6 0 000 12z"
                clip-rule="evenodd"
            />
        </svg>
    </div>
    {#if is_hover}
        <div
            class="absolute w-40 h-20 -bottom-12 flex justify-center items-center cursor-default"
            on:mouseleave={() => {
                is_hover = false;
            }}
        >
            {#each tools as tool}
                <div
                    class="w-fit h-3 mx-1 bg-gray-300 hover:bg-gray-50 dark:bg-gray-700 dark:hover:bg-gray-800 rounded flex justify-center items-center text-xs"
                >
                    {tool}
                </div>
            {/each}
        </div>
    {/if}
</div>
