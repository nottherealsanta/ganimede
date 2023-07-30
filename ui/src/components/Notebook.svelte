<script>
  import {
    cells,
    ydoc,
    cp_graph,
    pc_graph,
    np_graph,
    html_elements,
  } from "../stores/_notebook";

  import Edges from "./utility_components/Edges.svelte";

  function get_cell(id) {
    return ydoc.getMap(id);
  }

  function align_parent_less_cells() {
    let top = 1000;
    let left = 5000;
    for (let cell_id of $cells) {
      if ($cp_graph[cell_id]) {
        continue;
      }
      get_cell(cell_id).set("top", top);
      top += $html_elements[cell_id].offsetHeight + 10;
      get_cell(cell_id).set("left", left);
    }
    // window.scrollTo(4900, 1000)
    // scroll to the first cell
    window.scrollTo({
      top: get_cell($cells[0]).get("top") - 100,
      left: get_cell($cells[0]).get("left") - window.innerWidth / 2,
      behavior: "instant",
    });
    //
  }

  // wait for $cell to be defined
  let aligned = false;
  $: if ($cells !== undefined && $html_elements !== undefined && !aligned) {
    aligned = true;
    // call align_parent_less_cells() after 1 second
    console.log("get_cell($cells[0]).get", get_cell($cells[0]).get("top"));
    if (
      get_cell($cells[0]).get("top") === null ||
      get_cell($cells[0]).get("top") === undefined
    ) {
      setTimeout(align_parent_less_cells, 1000);
    }
  }

  // Components
  import Cell from "./Cell.svelte";
  import Tissue from "./Tissue.svelte";

  $: console.log("cells", $cells);
</script>

{#each $cells as cell_id}
  {#if !(cell_id in $pc_graph)}
    <Cell {cell_id} />
  {:else}
    <Tissue {cell_id} />
  {/if}
  {#if $np_graph[cell_id]}
    {#each $np_graph[cell_id] as next_id}
      <Edges current_cell_id={cell_id} {next_id} />
    {/each}
  {/if}
{/each}
