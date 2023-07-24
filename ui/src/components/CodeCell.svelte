<script>
    import { cells } from "../stores/_notebook";
    import Outputs from "./cell_components/Outputs.svelte";

    export let cell;

    import CodeEditor from "./cell_components/CodeEditor.svelte";
    let focus;

    import PrimeButton from "./cell_components/PrimeButton.svelte";
    import DeleteButton from "./cell_components/DeleteButton.svelte";
    import ExecutionCount from "./cell_components/ExecutionCount.svelte";

    import Drag from "../components/cell_components/Icons/drag.svelte";
    import MenuButton from "./cell_components/MenuButton.svelte";

    let is_hover = false;
</script>

<div
    class="flex flex-col min-w-[250px]"
    on:mouseenter={() => {
        is_hover = true;
    }}
    on:mouseleave={() => {
        is_hover = false;
    }}
>
    <div
        class="flex flex-col items-start w-auto h-auto rounded p-0.25justify-start align-middle"
    >
        <CodeEditor {cell} bind:focus />
        <!-- 
        <div
            class="flex h-2 w-fit ml-auto text-[9px] text-neutral-400 dark:text-neutral-500 italic"
        >
            <div class="h-full w-fit flex items-center">python</div>
        </div>-->
        {#if cell.outputs.length > 0 || cell.state == "running"}
            <Outputs {cell} />
        {/if}
    </div>
</div>
