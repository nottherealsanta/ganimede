<script lang="ts">
    export let cell_id;

    import { id_map, cells } from "../../../stores/notebook";

    function connector_click(e) {
        e.preventDefault();
        console.log("button click");
        console.log(e.target.id);
        e.stopPropagation();
    }

    let is_hover = false;

    import ToolbarSlot from "./ToolbarSlot.svelte";
    import Connector from "../Icons/connector.svelte";
    import Python from "../Icons/python.svelte";
    import Markdown from "../Icons/markdown.svelte";
    import Disconnect from "../Icons/disconnect.svelte";
    import NewCellMenu from "../Icons/newCellMenu.svelte";
    import { send_message } from "../../../stores/socket";

    function sendMessage(method, cellType) {
        send_message({
            channel: "notebook",
            method,
            message: {
                previous_cell_id: cell_id,
            },
        });
    }

    async function new_code_cell(e) {
        e.stopPropagation();
        e.preventDefault();
        console.log("new code cell", e);
        // sendMessage("new_code_cell", "code");
    }

    async function new_markdown_cell() {
        sendMessage("new_markdown_cell", "markdown");
    }
</script>

<div
    class="newcelltoolbar absolute -bottom-2 left-[25px] w-fit h-hit flex justify-center items-center"
>
    {#if is_hover}
        <div
            class="relative w-full h-5 z-50 -bottom-1 flex flex-row justify-center items-center cursor-default bg-oli dark:bg-oli-700 rounded border border-oli-300 dark:border-neutral-700 overflow-clip fill-oli-600 dark:fill-gray-300"
            style="transform: translateX(-46%); "
            on:mouseleave={() => {
                is_hover = false;
            }}
        >
            <ToolbarSlot><Disconnect /></ToolbarSlot>
            <ToolbarSlot on:click={new_code_cell}><Python /></ToolbarSlot>
            <ToolbarSlot><Connector /></ToolbarSlot>
            <ToolbarSlot on:click={new_markdown_cell}><Markdown /></ToolbarSlot>
            <ToolbarSlot><NewCellMenu /></ToolbarSlot>
        </div>
    {:else}
        <div
            class="w-3 h-3 rounded-full bg-oli-100 dark:bg-oli-700 flex justify-center items-center cursor-pointer stroke-oli-300 dark:stroke-oli-400 stroke-2"
            id="new-cell-toolbar"
            on:click|stopPropagation={connector_click}
            on:keydown={() => {}}
            on:mouseenter={() => {
                is_hover = true;
            }}
        >
            <Connector />
        </div>
    {/if}
</div>
