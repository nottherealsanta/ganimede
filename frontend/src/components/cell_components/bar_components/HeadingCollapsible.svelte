<script>
  import { ChevronDown, ChevronRight } from "lucide-svelte";

  import {
    ydoc,
    pc_graph,
    propagateCollapse,
    n_descendants,
  } from "../../../stores/notebook";

  export let cell;
  export let show;

  $: is_collapsed = cell.collapsed == "h";

  function get_number_of_descendants(cell_id) {
    let count = 0;
    if ($pc_graph[cell_id]) {
      count += $pc_graph[cell_id].length;
      for (let child_id of $pc_graph[cell_id]) {
        count += get_number_of_descendants(child_id);
      }
    }
    return count;
  }

  function toggleCollapse() {
    is_collapsed = !is_collapsed;
    // cell.collapsed = is_collapsed ? "h" : "";
    propagateCollapse(cell.id, is_collapsed);
    cell.ycell.set("collapsed", is_collapsed ? "h" : "");
  }
</script>

{#if (show || is_collapsed) && $n_descendants[cell.id] > 0}
  <!-- show number of descendants -->
  {#if is_collapsed}
    <span class="decendants">{$n_descendants[cell.id]}</span>
  {/if}
  <button
    class="toolbar-button {is_collapsed
      ? 'bg-blue-50 border-blue-100'
      : 'bg-transparent border-gray-100'}"
    on:click|stopPropagation={() => {
      toggleCollapse();
    }}
  >
    <!-- <div class=" {is_collapsed ? 'text-blue-500 -rotate-90' : 'text-gray-500'}"> -->
    <!-- </div> -->
    {#if is_collapsed}
      <ChevronRight size="18" class="text-blue-500" />
    {:else}
      <ChevronDown size="18" class="text-gray-500" />
    {/if}
  </button>
{/if}

<style>
  .toolbar-button {
    @apply relative flex 
    h-5 w-5 p-0.5
    items-center justify-center
    bg-transparent
    border 
    rounded-full
    text-gray-500;
  }
  .toolbar-button:hover {
    @apply bg-gray-50;
  }
  .decendants {
    @apply absolute 
    -left-2
    text-xs text-blue-500;
    font-family: "IBM Plex Mono", monospace;
    font-weight: 500;
    transform: translateX(-100%);
  }
</style>
