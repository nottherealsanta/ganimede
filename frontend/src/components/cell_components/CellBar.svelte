<script lang="ts">
  import { ChevronDown, FastForward, Sparkles, X } from "lucide-svelte";

  import { cell_maps } from "../../scripts/test_nb";
  import { active_cell_id } from "../../stores/notebook";
  import AiBar from "./AiBar.svelte";
  import CellRunButton from "./bar_components/CellRunButton.svelte";
  import CellContextButton from "./bar_components/CellContextButton.svelte";

  export let cell_id: string;
  let cell: any = cell_maps[cell_id];
  export let is_hover: boolean = false;
  $: is_active = $active_cell_id === cell_id;

  $: is_markdown = cell.type === "markdown";
  $: is_heading =
    is_markdown &&
    cell.source.some((line: string) => line.trim().startsWith("#"));

  // ai bar
  let ai_bar: boolean = false;
  $: if (!is_active) {
    ai_bar = false;
  }

  $: exe_count_test =
    cell.execution_count === undefined
      ? "[ ]"
      : cell.execution_count.toString();
</script>

<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
<div class="cell-bar {is_markdown ? 'bg-white' : 'bg-gray-50'}">
  {#if !is_markdown}
    <CellRunButton {cell} />
  {/if}

  {#if is_hover}
    {#if is_markdown && is_heading}
      <button class="toolbar-button">
        <ChevronDown size="16" class="text-gray-500" />
      </button>
      <button class="toolbar-button">
        <FastForward size="16" class="text-gray-500" />
      </button>
    {/if}

    {#if !is_markdown}
      <div class="cell-status-time">0s</div>
    {/if}
    <div class="flex-grow"></div>
    {#if !is_markdown}
      <div class="execution-count">{exe_count_test}</div>
    {/if}
    <div class="language-indicator">{cell.type}</div>

    <!-- AI Button -->
    <button
      class="toolbar-button {ai_bar ? 'text-fuchsia-500' : ''}"
      on:click={() => (ai_bar = !ai_bar)}
    >
      <Sparkles size="16" />
    </button>
  {:else}
    <div class="flex-grow"></div>
  {/if}

  <CellContextButton {is_hover} />
</div>
{#if ai_bar && is_active}
  <AiBar bind:ai_bar />
{/if}

<style>
  .cell-bar {
    @apply flex 
    -top-2
    w-full h-8
    px-0.5 py-1
    items-center
    
    rounded-t;
  }
  .language-indicator {
    @apply flex 
    h-7 w-fit px-2
    mx-1
    items-center justify-center
    cursor-default
    bg-transparent
    rounded-md
    text-xs
    text-gray-500;
    font-family: "IBM Plex Sans", sans-serif;
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
    text-gray-500;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 500;
    font-style: normal;
  }
  .execution-count {
    @apply flex absolute
    h-full w-8
    left-1/2
    items-center justify-center
    cursor-default
    bg-transparent
    text-xs text-gray-500;
    font-family: "IBM Plex Sans", sans-serif;
    font-weight: 500;
    font-style: normal;
  }
  .toolbar-button {
    @apply relative flex 
    h-7 w-7 p-1 
    items-center justify-center
    bg-transparent
    rounded-md
    text-gray-500;
  }
  .toolbar-button:hover {
    @apply bg-gray-100;
  }
  .toolbar-button:active {
    @apply text-gray-800;
  }
</style>
