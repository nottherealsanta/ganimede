<script>
  export let cell;
  export let cell_hover;

  function connector_click(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  let is_hover = false;

  // Components
  import { create_cell } from "../../../stores/_notebook.js";

  async function new_code_cell(e) {
    e.stopPropagation();
    create_cell("code", cell);
  }

  async function new_markdown_cell(e) {
    e.stopPropagation();
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
      if (drag_on_element !== null) {
        let next_cell_id = drag_on_element.getAttribute("cell_id");

        if (next_cell_id) {
          if (!ynp_graph.get(cell.id)) {
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
      class="absolute w-fit h-5 -top-[11px] flex flex-row bg-transparent fill-oli-500 dark:fill-gray-300 stroke-oli-500 dark:stroke-oli-400 stroke"
      on:mousedown|stopPropagation={() => {}}
    >
      <!-- <ToolbarSlot><Disconnect /></ToolbarSlot> -->
      <div
        class="w-5 h-5 p-0.5 mr-[1px] bg-oli hover:bg-oli-100 active:bg-yellow-100 fill-oli-500 rounded border border-oli-300 cursor-pointer drop-shadow-md justify-center items-center flex"
        on:click={new_code_cell}
        on:keydown={new_code_cell}
      >
        <svg
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          viewBox="0 0 40 40"
          width="70%"
          height="70%"
        >
          <rect x="10" y="0" width="20" height="40" rx="10" ry="5" />
          <rect x="0" y="10" width="40" height="20" rx="5" ry="10" />
          <circle cx="14.5" cy="5" r="1.85" stroke="white" />
          <circle cx="25.5" cy="35" r="1.85" stroke="white" />
          <line x1="10" y1="9.5" x2="20" y2="9.5" stroke="white" />
          <line x1="20" y1="30.5" x2="30" y2="30.5" stroke="white" />
          <path
            d="m 9.5,30 c 0,-10 2.5,-10 10,-10 8.5,0 11,0 11,-10"
            stroke="white"
          />
        </svg>
      </div>
      {#if has_parent}
        <div
          class="w-5 h-5 p-0.5 mr-[1px] bg-oli hover:bg-oli-100 active:bg-sky-200 fill-oli-500 rounded border border-oli-300 cursor-pointer drop-shadow-md justify-center items-center flex"
          on:mousedown={drag_mousedown}
          on:mouseup={drag_mouseup}
        >
          <svg
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            width="70%"
            height="70%"
          >
            <path
              d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 100-12 6 6 0 000 12z"
            /></svg
          >
        </div>
      {:else}
        <div
          class="w-5 h-5 p-0.5 mr-[1px] bg-oli fill-oli rounded border border-oli-100 stroke-none cursor-pointer drop-shadow-md justify-center items-center flex"
        >
          <svg
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            width="70%"
            height="70%"
          >
            <path
              d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 100-12 6 6 0 000 12z"
            /></svg
          >
        </div>
      {/if}
      <div
        class="w-5 h-5 p-0.5 mr-[1px] bg-oli hover:bg-oli-100 active:bg-green-100 fill-oli-500 rounded border border-oli-300 cursor-pointer drop-shadow-md justify-center items-center flex"
        on:click={new_markdown_cell}
        on:keydown={new_markdown_cell}
      >
        <svg
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          viewBox="11.3 9.1 33 33"
          width="70%"
          height="70%"
        >
          <path
            d="M 12.0 39.2 V 12.0 h 8.0 l 8.0 10.0 l 8.0 -10.0 h 8.0 v 27.2 H 36.0 V 23.6 L 28.0 33.6 L 20.0 23.6 v 15.6 z h 8.0 z"
          />
        </svg>
      </div>
    </div>
  {:else}
    <div
      class="absolute w-10 h-5 z-[9999] -top-[10px] left-[11px] rounded-full flex items-center justify-center bg-transparent cursor-pointer stroke-oli-300 dark:stroke-oli-200 stroke-2 fill-oli-100 dark:fill-oli-500"
      id="new-cell-toolbar"
      on:click|stopPropagation={connector_click}
      on:keydown={() => {}}
    >
      <svg
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        width="50%"
        height="50%"
      >
        <path
          d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 100-12 6 6 0 000 12z"
        /></svg
      >
    </div>
  {/if}
</div>

<svelte:window on:mouseup={drag_mouseup} on:mousemove={drag_mousemove} />
