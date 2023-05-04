<script lang="ts">
    import Cell from "./Cell.svelte";
    import { id_map, cells } from "../stores/notebook";
    import Outputs from "./cell_components/Outputs.svelte";

    export let cell_id;

    $: cell = $cells[$id_map[cell_id]];

    import CodeEditor from "./cell_components/CodeEditor.svelte";
    let focus;

    import PrimeButton from "./cell_components/PrimeButton.svelte";
</script>

<Cell {cell_id}>
    <div class="flex items-start w-full h-auto justify-center align-stretch">
        <PrimeButton {cell_id} />
        <CodeEditor {cell_id} bind:focus />
    </div>
    {#if cell.outputs.length > 0 || cell.state == "running"}
        <Outputs {cell_id} />
    {/if}
</Cell>
