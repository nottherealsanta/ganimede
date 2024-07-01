<script>
  import { ChevronDown } from "lucide-svelte";

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
    propagateCollapse(cell.id, is_collapsed);
    cell.collapsed = is_collapsed ? "h" : "";
  }
</script>

{#if (show || is_collapsed) && $n_descendants[cell.id] > 0}
  <button
    class="toolbar-button"
    on:click|stopPropagation={() => {
      toggleCollapse();
    }}
  >
    <div class=" {is_collapsed ? 'text-blue-500 -rotate-90' : 'text-gray-500'}">
      <ChevronDown size="16" />
    </div>
    <!-- show number of descendants -->
    {#if is_collapsed}
      <span class="text-xs text-blue-500"
        >{$n_descendants[cell.id]} Cells Hidden</span
      >
    {/if}
  </button>
{/if}

<style>
  .toolbar-button {
    @apply relative flex 
    h-7 w-fit p-1 
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
