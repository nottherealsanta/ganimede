<script>
  export let current_cell_id;
  export let next_id;

  import { ydoc, ynp_graph } from "../../stores/_notebook";

  $: c = ydoc.getMap(current_cell_id).toJSON();

  $: n = ydoc.getMap(next_id).toJSON();

  ydoc.getMap(current_cell_id).observe((event) => {
    c = event.target.toJSON();
  });
  ydoc.getMap(next_id).observe((event) => {
    n = event.target.toJSON();
  });

  function get_box(x) {
    return {
      left: x.left,
      right: x.left + x.width,
      top: x.top,
      bottom: x.top + x.height,
      center: {
        x: x.left + x.width / 2,
        y: x.top + x.height / 2,
      },
      width: x.width,
      height: x.height,
    };
  }

  $: curr = get_box(c);
  $: next = get_box(n);

  $: curr_anchor = {
    x: curr.center.x,
    y: curr.bottom,
  };
  $: next_anchor = {
    x: next.center.x,
    y: next.top,
  };

  $: top = curr_anchor.y > next_anchor.y ? next_anchor.y : curr_anchor.y;
  $: left = curr.left > next.left ? next.left : curr.left;
  $: width = Math.abs(curr.left - next.left) + Math.max(curr.width, next.width);
  $: height = Math.abs(curr_anchor.y - next_anchor.y);

  // path
  $: if (next_anchor.y - 50 < curr_anchor.y) {
    top -= 25;
    height += 50;
  }

  let path = "";
  $: path = `M ${curr.left + 32 - left} ${curr.bottom - top + 2}
                C ${curr.left + 32 - left} ${curr.bottom - top + 50},
                ${next.left + 25 - left} ${next.top - top - 50},
                ${next.left + 25 - left} ${next.top - top - 5}`;

  $: close =
    next.top - curr.bottom < 50 &&
    next.left - curr.left < 50 &&
    next.left - curr.left > -50;

  // line should start from current bottom, current left + 25 and end at next top, next left + 25
  $: line = {
    x1: curr.left + 32 - left,
    y1: curr.bottom - top + 5,
    x2: next.left + 32 - left,
    y2: next.top - top - 5,
  };

  // --- mouse pos
  import mouse_pos from "../../stores/mouse";

  let show_edge_toolbar = false;
  let edge_toolbar_pos = {
    x: 0,
    y: 0,
  };
  function edge_mouse_down() {
    show_edge_toolbar = true;
    edge_toolbar_pos = {
      x: $mouse_pos.x,
      y: $mouse_pos.y,
    };
  }

  function delete_edge() {
    console.log("delete_edge");
    show_edge_toolbar = false;
    const ynp_graph_array = ynp_graph.get(current_cell_id);
    let _index = ynp_graph_array.toJSON().indexOf(next_id);
    ynp_graph_array.delete(_index);
  }
</script>

<div
  class="bg-transparent"
  id="edge"
  style="
    position: absolute;
    top: {top}px; left: {left}px;
    width: {width}px; height: {height}px;
    pointer-events: none;
    "
>
  <svg
    height="100%"
    width="100%"
    style="position: absolute; top: 0; left: 0; pointer-events: none;"
  >
    <defs>
      <marker
        id="arrow_head_path"
        viewBox="0 -5 10 10"
        refX="5"
        refY="0"
        markerWidth="4"
        markerHeight="4"
        orient="auto"
        class="fill-oli-400 dark:fill-oli-400"
      >
        <path d="M0,-5L10,0L0,5" />
      </marker>
      <marker
        id="arrow_line"
        viewBox="0 -5 10 10"
        refX="5"
        refY="0"
        markerWidth="3"
        markerHeight="3"
        orient="auto"
        class="fill-oli-400/30 dark:fill-oli-200/30"
      >
        <path d="M0,-5L10,0L0,5" />
      </marker>
      <marker
        id="circle_marker"
        viewBox="0 0 10 10"
        refX="5"
        refY="5"
        markerWidth="5"
        markerHeight="5"
        orient="auto"
        class="fill-oli-400/30 dark:fill-oli-200/30"
      >
        <circle cx="5" cy="5" r="3" />
      </marker>
    </defs>
    {#if !close}
      <path
        d={path}
        class="stroke-oli-400 dark:stroke-oli-400 stroke-[2px] fill-transparent active:stroke-sky-400 hover:stroke-oli-400 pointer-events-auto"
        style={close ? "stroke-width: 2px;" : ""}
        marker-end="url(#arrow_head_path)"
        on:mousedown={edge_mouse_down}
      />
    {:else}
      <line
        x1={line.x1}
        y1={line.y1}
        x2={line.x2}
        y2={line.y2}
        class="stroke-neutral-500 stroke-[2px] fill-transparent hover:stroke-neutral-800 hover:dark:stroke-neutral-200"
        stroke-dasharray="5,5"
        stroke-opacity="0.5"
        marker-end="url(#arrow_line)"
      />
    {/if}
  </svg>
</div>

{#if show_edge_toolbar}
  <div
    class="h-fit w-fit px-0.25 z-[999] bg-oli dark:bg-oli-700 rounded drop-shadow-md absolute overflow-clip items-center justify-center flex"
    style="top: {edge_toolbar_pos.y}px; left: {edge_toolbar_pos.x}px; transform: translate(-50%, -50%);"
    on:mouseleave={() => (show_edge_toolbar = false)}
  >
    <div
      class="w-5 h-5 p-0.5 bg-oli dark:bg-oli-700 hover:bg-oli-100 dark:hover:bg-oli-700 active:bg-red-200 dark:active:bg-red-600 fill-oli-500 border border-oli-200 dark:border-oli-500 dark:fill-oli-100 rounded cursor-pointer justify-center items-center flex"
      on:click={delete_edge}
      on:keydown={delete_edge}
    >
      <svg
        height="12px"
        width="12px"
        version="1.1"
        id="Capa_1"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        viewBox="0 0 483.291 483.291"
        xml:space="preserve"
        ><g>
          <path
            d="M306.342,327.462v-171.61c48.527-23.973,82.08-73.852,82.096-131.542c0-13.404-10.853-24.272-24.264-24.272 c-13.395,0-24.264,10.861-24.264,24.258c-0.017,54.183-44.09,98.256-98.257,98.256c-54.183,0-98.272-44.089-98.272-98.289 C143.381,10.86,132.513,0,119.118,0C105.72,0,94.853,10.86,94.853,24.264c0,57.706,33.553,107.593,82.08,131.572v171.632 c-48.544,23.989-82.08,73.875-82.08,131.558c0,13.403,10.867,24.264,24.265,24.264c13.395,0,24.264-10.861,24.264-24.264 c0-54.168,44.09-98.266,98.256-98.289c54.184,0.022,98.273,44.12,98.273,98.289c0,13.403,10.868,24.264,24.264,24.264 c13.396,0,24.264-10.861,24.264-24.264C388.438,401.335,354.886,351.45,306.342,327.462z M225.461,313.158V170.133 c5.323,0.592,10.711,0.948,16.192,0.948c5.466,0,10.853-0.356,16.16-0.939v143.017c-5.324-0.585-10.71-0.948-16.177-0.948 C236.172,312.21,230.785,312.572,225.461,313.158z"
          ></path>
        </g></svg
      >
    </div>
    <div
      class="ml-1 w-5 h-5 p-0.5 bg-oli dark:bg-oli-700 hover:bg-oli-100 dark:hover:bg-oli-700 active:bg-red-200 dark:active:bg-red-600 fill-oli-500 border border-oli-200 dark:border-oli-500 dark:fill-oli-100 rounded cursor-pointer justify-center items-center flex"
      on:click={delete_edge}
      on:keydown={delete_edge}
    >
      <svg
        height="12px"
        width="12px"
        version="1.1"
        id="Capa_1"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        viewBox="0 0 460.775 460.775"
        xml:space="preserve"
        ><g>
          <path
            d="M285.08,230.397L456.218,59.27c6.076-6.077,6.076-15.911,0-21.986L423.511,4.565c-2.913-2.911-6.866-4.55-10.992-4.55 c-4.127,0-8.08,1.639-10.993,4.55l-171.138,171.14L59.25,4.565c-2.913-2.911-6.866-4.55-10.993-4.55 c-4.126,0-8.08,1.639-10.992,4.55L4.558,37.284c-6.077,6.075-6.077,15.909,0,21.986l171.138,171.128L4.575,401.505 c-6.074,6.077-6.074,15.911,0,21.986l32.709,32.719c2.911,2.911,6.865,4.55,10.992,4.55c4.127,0,8.08-1.639,10.994-4.55 l171.117-171.12l171.118,171.12c2.913,2.911,6.866,4.55,10.993,4.55c4.128,0,8.081-1.639,10.992-4.55l32.709-32.719 c6.074-6.075,6.074-15.909,0-21.986L285.08,230.397z"
          ></path>
        </g></svg
      >
    </div>
  </div>
{/if}
