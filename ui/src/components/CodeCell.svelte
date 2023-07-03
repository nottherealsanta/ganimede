<script lang="ts">
    import { id_map, cells } from "../stores/notebook";
    import Outputs from "./cell_components/Outputs.svelte";

    export let cell_id;

    $: cell = $cells[$id_map[cell_id]];

    import CodeEditor from "./cell_components/CodeEditor.svelte";
    let focus;

    import PrimeButton from "./cell_components/PrimeButton.svelte";
</script>

<div class="flex flex-row p-0.5">
    <div class="flex h-full w-fit pt-0.25 pr-0.5 items-center justify-center">
        <PrimeButton {cell_id} />
    </div>
    <div
        class="flex flex-col items-start w-auto h-auto justify-start align-middle"
    >
        <CodeEditor {cell_id} bind:focus />

        <div
            class="flex h-2 w-fit ml-auto text-[9px] text-neutral-400 dark:text-neutral-500 italic"
        >
            <div class="h-full w-fit flex items-center">python</div>
        </div>

        {#if cell.outputs.length > 0 || cell.state == "running"}
            <Outputs {cell_id} />
        {/if}
    </div>
</div>
