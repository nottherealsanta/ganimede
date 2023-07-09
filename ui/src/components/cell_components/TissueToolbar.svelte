<script>
    export let cell_id;

    import PrimeButton from "../cell_components/PrimeButton.svelte";
    import DeleteButton from "../cell_components/DeleteButton.svelte";
    import ExecutionCount from "../cell_components/ExecutionCount.svelte";
    import DragTissue from "./DragTissue.svelte";

    import Drag from "../cell_components/Icons/drag.svelte";
    import MenuButton from "../cell_components/MenuButton.svelte";

    import { id_map, cells, pc_graph } from "../../stores/notebook";

    $: cell = $cells[$id_map[cell_id]];

    export let is_hover = false;
</script>

<div
    class="flex bg-oli-100 dark:bg-oli-800 h-6 w-full rounded-t p-0.5 cursor-grab active:cursor-grabbing"
    on:mousedown
    on:mosueup
>
    {#if $cells[$id_map[cell_id]].type === "code" || cell_id in $pc_graph}
        <PrimeButton {cell_id} />
        <!-- <ExecutionCount {cell_id} /> -->
    {:else}
        <div class="h-5 w-5" />
    {/if}
    {#if is_hover}
        <Drag />
        <div class="flex flex-row ml-auto">
            <DeleteButton {cell_id} />
            <MenuButton {cell_id} />
        </div>
    {/if}
</div>
