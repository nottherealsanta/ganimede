<script lang="ts">
    export let cell_id;

    import { id_map, cells } from "../../../stores/notebook";
    $: cell = $cells[$id_map[cell_id]];

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

    async function new_code_cell() {
        sendMessage("new_code_cell", "code");
    }

    async function new_markdown_cell() {
        sendMessage("new_markdown_cell", "markdown");
    }
</script>

<div
    class="newcelltoolbar absolute -bottom-0 left-0 w-full h-0 flex justify-center items-center"
>
    {#if is_hover}
        <div
            class="relative w-40 h-4 -bottom-0 flex flex-row justify-center items-center cursor-default bg-oli dark:bg-vs-dark rounded border border-gray-300 dark:border-neutral-700 overflow-clip fill-gray-700 dark:fill-gray-300"
            on:mouseleave={() => {
                is_hover = false;
            }}
        >
            <ToolbarSlot on:click={new_code_cell}><Python /></ToolbarSlot>
            <ToolbarSlot on:click={new_markdown_cell}><Markdown /></ToolbarSlot>
            <ToolbarSlot><Connector /></ToolbarSlot>
            <ToolbarSlot><Disconnect /></ToolbarSlot>
            <ToolbarSlot><NewCellMenu /></ToolbarSlot>
        </div>
    {:else}
        <div
            class="absolute w-3 h-3 rounded-full bg-oli-50/50 dark:bg-oli-700/50 flex justify-center items-center cursor-pointer fill-oli-200 dark:fill-oli-500 stroke-oli-600/20 dark:stroke-oli-50/20 stroke-2"
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
