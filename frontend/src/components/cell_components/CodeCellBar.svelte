<script lang="ts">
  import { Sparkles, X } from "lucide-svelte";

  import { cell_maps } from "../../scripts/test_nb";
  import { activeCellId } from "../../stores/notebook";
  import AiBar from "./AiBar.svelte";
  import CellRunButton from "./bar_components/CellRunButton.svelte";
  import CellContextButton from "./bar_components/CellContextButton.svelte";

  export let cell_id: string;
  let cell: any = cell_maps[cell_id];
  export let is_hover: boolean = false;
  $: is_active = $activeCellId === cell_id;

  // ai bar
  let ai_bar: boolean = false;
  $: if (!is_active) {
    ai_bar = false;
  }
</script>

<div class="cell-sidebar">
  <CellRunButton {cell} {is_hover} />
  <div class="flex-grow"></div>
  {#if is_hover}
    <div class="cell-status-time">0.0s</div>
    <div class="language-indicator">{cell.type}</div>
    <button
      class="toolbar-button {ai_bar ? 'text-fuchsia-500' : ''}"
      on:click={() => (ai_bar = !ai_bar)}
      aria-label="Toggle AI Bar"
    >
      {#if ai_bar}
        <X size="16" />
      {:else}
        <Sparkles size="16" />
      {/if}
    </button>
  {/if}
  <CellContextButton {is_hover} />
</div>
{#if ai_bar && is_active}
  <AiBar {ai_bar} />
{/if}

<style>
  .cell-sidebar {
    @apply flex 
    w-full h-8
    px-1 py-0.5
    items-center
    bg-transparent
    rounded-t;
  }
  .language-indicator {
    @apply flex 
    h-full w-fit px-1
    mr-2
    items-center justify-center
    cursor-default
    bg-gray-50
    rounded-md
    text-xs
    text-gray-400;
    font-family: "Inter", sans-serif;
    font-weight: 500;
    font-style: normal;
  }
  .language-indicator:hover {
    @apply bg-gray-100;
  }
  .cell-status-time {
    @apply flex 
    h-full w-16
    items-center justify-center
    cursor-default
    bg-transparent
    text-xs
    text-gray-400;
    font-family: "Inter", sans-serif;
    font-weight: 500;
    font-style: normal;
  }
  .execution-count {
    @apply flex 
    h-full w-8
    items-center justify-center
    cursor-default
    bg-transparent
    text-xs text-gray-400;
    font-family: "Inter", sans-serif;
    font-weight: 500;
    font-style: normal;
  }
  .toolbar-button {
    @apply relative flex 
    h-7 w-7 p-1 
    items-center justify-center
    bg-transparent
    rounded-md
    text-gray-400;
  }
  .toolbar-button:hover {
    @apply bg-gray-100;
  }
  .toolbar-button:active {
    @apply text-gray-800;
  }
</style>
