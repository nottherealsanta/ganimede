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

  $: is_parent_less = $cp_graph[cell.id] === undefined;

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
    drag_start_pos = { x: $mouse_pos.x, y: $mouse_pos.y };
    drag_line = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    drag_line.setAttribute(
      "class",
      "absolute bg-transparent w-full h-full top-0 left-0 z-50 pointer-events-none",
    );
    drag_line.setAttribute("style", "z-index: 9999;");
    canvas_div = document.getElementById("canvas");
    canvas_div.appendChild(drag_line);
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
  class="newcelltoolbar absolute -bottom-[21px] -left-[1px] w-fit h-5 z-[9999]"
  on:mouseenter={() => {
    is_hover = true;
  }}
  on:mouseleave={() => {
    is_hover = false;
  }}
  style="opacity: {cell_hover ? 1 : 0}; "
>
  {#if is_hover}
    <div
      class="absolute w-fit h-fit -top-[11px] z-[9999] flex flex-row rounded bg-oli dark:bg-oli-800 drop-shadow-md border border-oli-400 overflow-clip items-center justify-center fill-oli-500 dark:fill-oli stroke-oli-500 dark:stroke-oli-400 stroke"
      on:mousedown|stopPropagation={() => {}}
    >
      <!-- <ToolbarSlot><Disconnect /></ToolbarSlot> -->
      <div
        class="w-5 h-5 p-0.5 bg-oli dark:bg-oli-700 hover:bg-oli-100 dark:hover:bg-oli-700 active:bg-yellow-100 fill-oli-400 dark:fill-oli cursor-pointer justify-center items-center flex"
        on:click={new_code_cell}
        on:keydown={new_code_cell}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          aria-label="Python"
          role="img"
          viewBox="0 0 512 512"
          width="90%"
          height="90%"
          ><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g
            id="SVGRepo_tracerCarrier"
            stroke-linecap="round"
            stroke-linejoin="round"
          ></g><g id="SVGRepo_iconCarrier">
            <g>
              <path
                id="p"
                d="M254 64c-16 0-31 1-44 4-39 7-46 21-46 47v35h92v12H130c-27 0-50 16-58 46-8 35-8 57 0 93 7 28 23 47 49 47h32v-42c0-30 26-57 57-57h91c26 0 46-21 46-46v-88c0-24-21-43-46-47-15-3-32-4-47-4zm-50 28c10 0 17 8 17 18 0 9-7 17-17 17-9 0-17-8-17-17 0-10 8-18 17-18z"
              ></path>
            </g>
            <use xlink:href="#p" transform="rotate(180,256,255)"></use>
          </g></svg
        >
      </div>
      {#if is_parent_less}
        <div
          class="z-[999] w-5 h-5 p-0.5 bg-oli dark:bg-oli-700 hover:bg-oli-100 dark:hover:bg-oli-700 active:bg-sky-200 fill-oli-400 dark:fill-oli stroke-none cursor-pointer justify-center items-center flex"
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
          class="w-5 h-5 p-0.5 bg-oli-50 dark:bg-oli-700 rounded border border-oli-100 dark:border-oli-500 justify-center items-center flex"
        ></div>
      {/if}
      <div
        class="w-5 h-5 p-0.5 bg-oli dark:bg-oli-700 hover:bg-oli-100 dark:hover:bg-oli-700 active:bg-green-100 fill-oli-400 stroke-none dark:fill-oli cursor-pointer justify-center items-center flex"
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
      class="absolute w-10 h-5 z-[9999] -top-[10px] left-[11px] rounded-full flex items-center justify-center bg-transparent cursor-pointer stroke-oli-300 dark:stroke-oli-500 stroke-2 fill-oli-100 dark:fill-oli-500"
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
