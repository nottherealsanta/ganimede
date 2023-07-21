<script>
    import { fetchConfig, config } from "./stores/config.js";
    import Canvas from "./components/Canvas.svelte";

    async function loadApp() {
        await fetchConfig();
    }

    // override "id"  in svelte-dnd-action to "_id"
    import { overrideItemIdKeyNameBeforeInitialisingDndZones } from "svelte-dnd-action";
    overrideItemIdKeyNameBeforeInitialisingDndZones("_id");

    import { onMount } from "svelte";

  

</script>

{#await loadApp()}
    <div>Loading...</div>
{:then}
    <Canvas />
    {/await}
