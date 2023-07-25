<script>
    import RunIcon from "../cell_components/Icons/run.svelte";
    import DeleteIcon from "../cell_components/Icons/delete.svelte";
    import PlusIcon from "../cell_components/Icons/plus.svelte";
    import CommitIcon from "../cell_components/Icons/commit.svelte";
    import MoreIcon from "../cell_components/Icons/more.svelte";
    import PrimeButton from "../cell_components/PrimeButton.svelte";
    import DeleteButton from "../cell_components/DeleteButton.svelte";
    import ExecutionCount from "../cell_components/ExecutionCount.svelte";

    import Drag from "../cell_components/Icons/drag.svelte";
    import MenuButton from "../cell_components/MenuButton.svelte";

    import { cells, pc_graph } from "../../stores/_notebook";

    export let cell;

    export let is_hover = false;
</script>

<div
    class="bg-oli-50 dark:bg-oli-600 rounded-t flex h-fit w-full p-0.5  border-b border-oli-200 dark:border-oli-400  cursor-grab active:cursor-grabbing"
>
    {#if cell.type === "code" || cell.id in $pc_graph}
        <PrimeButton {cell} />
        <!-- <ExecutionCount {cell} /> -->
    {:else}
        <div class="h-5 w-5" />
    {/if}
    {#if is_hover}
        <Drag />
        <div class="flex flex-row ml-auto">
            <DeleteButton {cell} />
            <MenuButton {cell} />
        </div>
    {/if}
</div>
