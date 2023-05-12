<script>
    export let cell_id;

    import RunIcon from "../cell_components/Icons/run.svelte";
    import DeleteIcon from "../cell_components/Icons/delete.svelte";
    import PlusIcon from "../cell_components/Icons/plus.svelte";
    import CommitIcon from "../cell_components/Icons/commit.svelte";
    import MoreIcon from "../cell_components/Icons/more.svelte";

    import { id_map, cells } from "../../stores/notebook";
    $: cell = $cells[$id_map[cell_id]];
    $: is_tissue = cell.source[0] ? cell.source[0].startsWith("#") : false;

    const button_class =
        "h-[25px] w-[25px] m-[1px] bg-white hover:bg-gray-100 active:bg-gray-200 rounded inline-flex items-center border-2 justify-center border-gray-200 dark:bg-neutral-800 dark:hover:bg-neutral-700 dark:active:bg-neutral-600 dark:text-neutral-100 dark:border-neutral-700";
</script>

<div
    class="
    bg-transparent w-fit h-fit pt-0.5 pb-0.5 rounded-md fill-gray-600 dark:fill-gray-300
    absolute flex flex-col justify-left items-center z-10"
    style="right: -{is_tissue ? 29 : 27}px; top: -5px;"
>
    {#if is_tissue}
        <div class={button_class}><RunIcon /></div>
    {/if}
    <div class={button_class}><DeleteIcon /></div>
    <!-- <div class={button_class}><PlusIcon /></div> -->
    <div class={button_class}><CommitIcon /></div>
    <div class={button_class}><MoreIcon /></div>
</div>
