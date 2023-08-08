<script>
  export let cell;
  export let cell_hover;

  function connector_click(e) {
    e.preventDefault();
    console.log("button click");
    console.log(e.target.id);
    e.stopPropagation();
  }

  let is_hover = false;

  // Components
  import ToolbarSlot from "./ToolbarSlot.svelte";
  import Connector from "../Icons/connector.svelte";
  import Python from "../Icons/python.svelte";
  import Markdown from "../Icons/markdown.svelte";
  import Disconnect from "../Icons/disconnect.svelte";
  import NewCellMenu from "../Icons/newCellMenu.svelte";
  import { create_cell } from "../../../stores/_notebook.js";

  async function new_code_cell(e) {
    create_cell("code", cell);
  }

  async function new_markdown_cell() {
    create_cell("markdown", cell);
  }

  $: has_parent = $cp_graph[cell.id] === undefined;

  // ---- canvas div
  let canvas_div = null;

  // ---- next prev dragging
  import mouse_pos from "../../../stores/mouse.js";
  import { cp_graph, ynp_graph } from "../../../stores/_notebook.js";
  import * as Y from "yjs";

  let dragging = false;
  let drag_on_element = null;
  let drag_start_pos = { x: null, y: null };
  let drag_end_pos = { x: null, y: null };
  let drag_line = null;

  function drag_mousedown() {
    dragging = true;
    console.log("drag_mousedown");
    drag_start_pos = { x: $mouse_pos.x, y: $mouse_pos.y };
    drag_line = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    drag_line.setAttribute(
      "class",
      "absolute bg-transparent w-full h-full top-0 left-0 z-50 pointer-events-none",
    );
    drag_line.setAttribute("style", "z-index: 9999;");
    canvas_div = document.getElementById("canvas");
    canvas_div.appendChild(drag_line);
    console.log("drag_line", drag_line);
  }
  function drag_mousemove(e) {
    if (!dragging) {
      return;
    }
    const elements_under = document.elementsFromPoint(e.clientX, e.clientY);
    const cells_tissues_under = elements_under.filter(
      (el) => el.classList.contains("cell") || el.classList.contains("tissue"),
    );
    const cells_tissues_under_reverse = cells_tissues_under.reverse();

    // first cell or tissue that does not have a parent
    const first_parent_less = cells_tissues_under_reverse.find(
      (el) => !cp_graph[el.getAttribute("cell_id")],
    );

    // first_parent_less cannot be the cell itself
    if (
      first_parent_less &&
      first_parent_less.getAttribute("cell_id") === cell.id
    ) {
      return;
    }

    // create drag indicator that has top, left, width, height of first_parent_less
    if (first_parent_less) {
      if (drag_on_element === null) {
        drag_on_element = document.createElement("div");
        drag_on_element.classList.add("drag-indicator");
        drag_on_element.style.position = "absolute";
        drag_on_element.style.top = first_parent_less.offsetTop + "px";
        drag_on_element.style.left = first_parent_less.offsetLeft + "px";
        drag_on_element.style.width = first_parent_less.offsetWidth + "px";
        drag_on_element.style.height = first_parent_less.offsetHeight + "px";
        drag_on_element.style.backgroundColor = "#29B0F822";
        drag_on_element.style.border = "2px solid #29B0F8";
        drag_on_element.style.zIndex = "9999";
        drag_on_element.setAttribute(
          "cell_id",
          first_parent_less.getAttribute("cell_id"),
        );
        canvas_div.appendChild(drag_on_element);
      } else {
        drag_on_element.style.top = first_parent_less.offsetTop + "px";
        drag_on_element.style.left = first_parent_less.offsetLeft + "px";
        drag_on_element.style.width = first_parent_less.offsetWidth + "px";
        drag_on_element.style.height = first_parent_less.offsetHeight + "px";
      }
    } else {
      if (drag_on_element !== null) {
        canvas_div.removeChild(drag_on_element);
        drag_on_element = null;
      }
    }

    drag_end_pos = { x: $mouse_pos.x, y: $mouse_pos.y };
    console.log("drag_end_pos:", drag_end_pos);
    drag_line.innerHTML = `
      <line
        x1=${drag_start_pos.x}
        y1=${drag_start_pos.y}
        x2=${drag_end_pos.x}
        y2=${drag_end_pos.y}
        stroke="#29B0F8"
        stroke-width="2"
        stroke-dasharray="8 4"
        stroke-dashoffset="0"
      />
    `;
  }
  function drag_mouseup() {
    if (dragging) {
      dragging = false;
      console.log("drag_mouseup");
      if (drag_on_element !== null) {
        let next_cell_id = drag_on_element.getAttribute("cell_id");

        if (next_cell_id) {
          console.log("next_cell_id", next_cell_id);
          if (!ynp_graph.get(cell.id)) {
            console.log("ynp_graph.get(cell.id)", ynp_graph.get(cell.id));
            ynp_graph.set(cell.id, new Y.Array());
          }
          ynp_graph.get(cell.id).push([next_cell_id]);
        }

        canvas_div.removeChild(drag_on_element);
        drag_on_element = null;
      }
      drag_start_pos = { x: null, y: null };
      drag_end_pos = { x: null, y: null };
      if (drag_line !== null) {
        canvas_div.removeChild(drag_line);
        drag_line = null;
      }
    }
  }
</script>

<div
  class="newcelltoolbar absolute -bottom-[21px] w-fit h-5 bg-transparent"
  on:mouseenter={() => {
    is_hover = true;
  }}
  on:mouseleave={() => {
    is_hover = false;
  }}
  style="opacity: {cell_hover ? 1 : 0}; transition: opacity 0.1s ease-in-out;"
>
  {#if is_hover}
    <div
      class="absolute w-fit h-[19px] z-[9999] -top-[10px] flex flex-row drop-shadow-md cursor-default bg-oli dark:bg-oli-700 rounded border border-oli-500 dark:border-oli-300 overflow-clip fill-oli-500 dark:fill-gray-300 stroke-oli-500 dark:stroke-oli-400 stroke"
      on:mousedown|stopPropagation={() => {}}
    >
      <!-- <ToolbarSlot><Disconnect /></ToolbarSlot> -->
      <ToolbarSlot on:click={new_code_cell}><Python /></ToolbarSlot>
      {#if has_parent}
        <Connector
          on:mousedown={drag_mousedown}
          on:mousemove={drag_mousemove}
          on:mouseup={drag_mouseup}
        />
      {:else}
        <ToolbarSlot></ToolbarSlot>
      {/if}
      <ToolbarSlot on:click={new_markdown_cell}><Markdown /></ToolbarSlot>
      <!-- <ToolbarSlot><NewCellMenu /></ToolbarSlot> -->
    </div>
  {:else}
    <div
      class="absolute w-3 h-5 z-[9999] -top-[10px] left-[25px] rounded-full flex items-center justify-center bg-transparent cursor-pointer stroke-oli-300 dark:stroke-oli-200 stroke-2 fill-oli-100 dark:fill-oli-500"
      id="new-cell-toolbar"
      on:click|stopPropagation={connector_click}
      on:keydown={() => {}}
    >
      <svg
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        width="80%"
        height="80%"
      >
        <path
          d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 100-12 6 6 0 000 12z"
        /></svg
      >
    </div>
  {/if}
</div>

<svelte:window on:mouseup={drag_mouseup} on:mousemove={drag_mousemove} />

<!-- a line from the cell to the new cell toolbar -->
<!-- {#if drag_start_pos.x !== null && drag_start_pos.y !== null}
  <svg
    class="absolute bg-red-300 w-full h-full top-0 left-0 z-50 pointer-events-none"
  >
    <line
      x1={drag_start_pos.x}
      y1={drag_start_pos.y}
      x2={drag_end_pos.x}
      y2={drag_end_pos.y}
      stroke="#29B0F8"
      stroke-width="2"
    />
  </svg>
{/if} -->
