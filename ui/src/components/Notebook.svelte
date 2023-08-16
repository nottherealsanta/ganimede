<script>
  import {
    ycells,
    ydoc,
    ynp_graph,
    cp_graph,
    pc_graph,
    html_elements,
  } from "../stores/_notebook";

  import Edges from "./utility_components/Edges.svelte";

  // Components
  import Cell from "./Cell.svelte";
  import Tissue from "./Tissue.svelte";

  let cells = ycells.toJSON();
  let cells_map = [];
  cells_map = cells.map((cell, index) => ({
    serial: index + 1,
    cell_id: cell,
  }));

  ycells.observe((event) => {
    cells = ycells.toJSON();
    // cells = cells;
  });

  let np_graph = ynp_graph.toJSON();
  ynp_graph.observeDeep((event) => {
    np_graph = ynp_graph.toJSON();
  });
  $: np_graph = np_graph;

  function get_cell(id) {
    return ydoc.getMap(id);
  }

  function align_parent_less_cells() {
    console.log("000", ydoc.getMap("notebook").get("aligned"));
    if (!ydoc.getMap("notebook").get("aligned")) {
      let top = 1000;
      let left = 5000;
      for (let cell_id of cells) {
        if ($cp_graph[cell_id]) {
          continue;
        }
        get_cell(cell_id).set("top", top);
        top += $html_elements[cell_id].offsetHeight + 10;
        get_cell(cell_id).set("left", left);
      }
      // window.scrollTo(4900, 1000)
      // scroll to the first cell
    }
    ydoc.getMap("notebook").set("aligned", true);
    window.scrollTo({
      top: get_cell(cells[0]).get("top") - 100,
      left: get_cell(cells[0]).get("left") - 100,
      behavior: "instant",
    });
  }

  // wait for $cell to be defined
  let aligned = false;
  $: if (
    ycells !== undefined &&
    cells !== undefined &&
    $html_elements !== undefined &&
    !aligned
  ) {
    aligned = true;
    // call align_parent_less_cells() after 1 second
    setTimeout(align_parent_less_cells, 1000);
  }
</script>

{#each cells as cell_id, index (cell_id)}
  {#if !(cell_id in $pc_graph)}
    <Cell {cell_id} />
  {:else}
    <Tissue {cell_id} />
  {/if}
{/each}

{#each cells as cell_id, index (cell_id)}
  {#if np_graph[cell_id]}
    {#each np_graph[cell_id] as next_id}
      <Edges current_cell_id={cell_id} {next_id} />
    {/each}
  {/if}
{/each}
