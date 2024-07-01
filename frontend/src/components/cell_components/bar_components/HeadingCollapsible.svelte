<script>
  import { ChevronDown } from "lucide-svelte";

  import { ydoc, pc_graph } from "../../../stores/notebook";

  export let cell;
  export let show;

  $: is_collapsed = cell.collapsed == "h";

  function propagateCollapse(cell_id, state) {
    // If the cell has children, propagate the state to them
    if ($pc_graph[cell_id]) {
      if (ydoc.getMap(cell_id).collapsed != "h") {
        for (let child_id of $pc_graph[cell_id]) {
          ydoc.getMap(child_id).set("parent_collapsed", state);
          propagateCollapse(child_id, state);
        }
      }
    }
  }

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

  let descendants = get_number_of_descendants(cell.id);

  $: if (is_collapsed) {
    descendants = get_number_of_descendants(cell.id);
  }

  function toggleCollapse() {
    is_collapsed = !is_collapsed;
    propagateCollapse(cell.id, is_collapsed);
    cell.collapsed = is_collapsed ? "h" : "v";
  }
</script>

{#if show || is_collapsed}
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
      <span class="text-xs text-blue-500">{descendants} Cells Hidden</span>
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
