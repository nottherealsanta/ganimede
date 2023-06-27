<script lang="ts">
    import { id_map, cells } from "../stores/notebook";
    import Outputs from "./cell_components/Outputs.svelte";

    export let cell_id;

    $: cell = $cells[$id_map[cell_id]];

    import CodeEditor from "./cell_components/CodeEditor.svelte";
    let focus;

    import PrimeButton from "./cell_components/PrimeButton.svelte";
</script>

<div>
    <div class="flex items-start w-auto h-auto justify-start align-middle">
        <PrimeButton {cell_id} />
        <CodeEditor {cell_id} bind:focus />
    </div>
    {#if cell.outputs.length > 0 || cell.state == "running"}
        <Outputs {cell_id} />
    {/if}
</div>
