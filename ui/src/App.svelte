<script>
	import { fetchConfig, config } from "./stores/config.js";
	import Canvas from "./components/Canvas.svelte";

	async function loadApp() {
		await fetchConfig();
	}
</script>

{#await loadApp()}
	<div>Loading...</div>
{:then}
	<Canvas />
{/await}
