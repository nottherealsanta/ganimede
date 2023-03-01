<script lang="ts">
    import Cell from "./Cell.svelte";

    import { notebook } from "../stores/notebook";
</script>

<div class="notebook">
    {#await notebook.get() then}
        {#each $notebook["cells"] as cell}
            <Cell cell_id={cell.id} />
        {/each}
    {/await}
</div>

<style>
    .notebook {
        display: flex;
    }
</style>
