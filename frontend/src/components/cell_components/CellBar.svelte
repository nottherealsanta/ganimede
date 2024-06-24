<script lang="ts">
  import AiBar from "./AiBar.svelte";
  import RunButton from "./bar_components/RunButton.svelte";
  import ContextButton from "./bar_components/ContextButton.svelte";
  import HeadingCollapsible from "./bar_components/HeadingCollapsible.svelte";
  import HeadingRunAll from "./bar_components/HeadingRunAll.svelte";
  import ExecutionTime from "./bar_components/ExecutionTime.svelte";
  import ExecutionCount from "./bar_components/ExecutionCount.svelte";
  import LanguageIndicator from "./bar_components/LanguageIndicator.svelte";
  import AIButton from "./bar_components/AIButton.svelte";

  import { ChevronDown, FastForward, Sparkles, X } from "lucide-svelte";

  import { cell_maps } from "../../scripts/test_nb";
  import { active_cell_id } from "../../stores/notebook";

  export let cell_id: string;
  let cell: any = cell_maps[cell_id];
  export let is_hover: boolean = false;
  $: is_active = $active_cell_id === cell_id;

  $: is_markdown = cell.type === "markdown";
  $: is_heading =
    is_markdown &&
    cell.source.some((line: string) => line.trim().startsWith("#"));

  // ai bar
  let is_ai_bar_open: boolean = false;
  $: if (!is_active) {
    is_ai_bar_open = false;
  }

  $: execution_count = cell.execution_count;
</script>

<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
<div class="cell-bar {is_markdown ? 'bg-white' : 'bg-gray-50'}">
  {#if !is_markdown}
    <RunButton {cell} />
  {/if}
  {#if is_markdown && is_heading}
    <HeadingCollapsible {is_heading} />
  {/if}

  {#if is_hover || is_active}
    {#if is_markdown && is_heading}
      <HeadingRunAll {is_heading} />
    {/if}

    {#if !is_markdown}
      <ExecutionTime {is_markdown} />
    {/if}
    <div class="flex-grow"></div>
    {#if !is_markdown}
      <ExecutionCount {execution_count} {is_markdown} />
    {/if}
    <LanguageIndicator cell_type={cell.type} />
    <AIButton bind:is_ai_bar_open />
  {:else}
    <div class="flex-grow"></div>
  {/if}

  <ContextButton {is_hover} {is_active} />
</div>
{#if is_ai_bar_open && is_active}
  <AiBar bind:is_ai_bar_open />
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
