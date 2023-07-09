<script>
    export let cell_id;

    import { cells, id_map } from "../../stores/notebook";

    $: cell = $cells[$id_map[cell_id]];
    let execution_count;
    $: if (cell) {
        if (cell.execution_count === null) {
            execution_count = "[ ]";
        } else {
            execution_count = cell.execution_count;
        }
    }
</script>

<div
    class="flex flex-none text-[0.68rem] bg-transparent font-mono active:bg-oli-200 dark:active:bg-oli-700 w-5 h-5 p-0 m-0 rounded-sm items-center justify-center text-oli-500 dark:text-oli-400"
>
    {execution_count}
</div>
