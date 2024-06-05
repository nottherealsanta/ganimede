<script>
  import {
    ycells,
    ydoc,
    ynp_graph,
    cp_graph,
    pc_graph,
    html_elements,
    // users,
    awareness,
  } from "../stores/_notebook";
  import mouse_pos from "../stores/mouse.js";
  import Edges from "./utility_components/Edges.svelte";

  // Components
  import Cell from "./Cell.svelte";
  import Tissue from "./Tissue.svelte";
  import { onMount } from "svelte";
  import Cursor from "./utility_components/Cursor.svelte";

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
    console.log("aligned: ", ydoc.getMap("notebook").get("aligned"));
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

  // ---------- awareness
  onMount(() => {
    awareness.setLocalStateField("cursor", {
      x: $mouse_pos.x,
      y: $mouse_pos.y,
    });
  });
  function mousemove(e) {
    awareness.setLocalStateField("cursor", {
      x: $mouse_pos.x,
      y: $mouse_pos.y,
    });
  }

  let users = [];
  let local_user_id = awareness.clientID;
  console.log("users: ", users);

  function update_users() {
    users = [];
    for (let [key, value] of awareness.getStates()) {
      if (key !== local_user_id) {
        users.push(value);
      }
    }
  }
  function debounce(func, delay) {
    let timer = null;

    return function () {
      clearTimeout(timer);
      timer = setTimeout(func, delay);
    };
  }

  const debouncedUpdateUsers = debounce(update_users, 10);

  awareness.on("change", (changes) => {
    debouncedUpdateUsers();
  });
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

<!-- awareness cursor -->
{#if users}
  {#each users as user}
    <Cursor
      x={user.cursor.x}
      y={user.cursor.y}
      id={user.id}
      color={user.color}
    />
  {/each}
{/if}

<svelte:window on:mousemove={mousemove} />
