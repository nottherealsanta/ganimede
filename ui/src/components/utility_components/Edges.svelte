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
  $: path = `M ${curr.left + 32 - left} ${curr.bottom - top + 5}
                C ${curr.left + 32 - left} ${curr.bottom - top + 50}, 
                ${next.left + 25 - left} ${next.top - top - 50}, 
                ${next.left + 25 - left} ${next.top - top - 5}`;

  $: close =
    next.top - curr.bottom < 100 &&
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
  class="bg-transparent z-[9998]"
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
        id="arrow_path"
        viewBox="0 -5 10 10"
        refX="5"
        refY="0"
        markerWidth="4"
        markerHeight="4"
        orient="auto"
        class="fill-oli-500 dark:fill-oli-200"
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
        class="stroke-oli-500 dark:stroke-oli-200 stroke-[2px] fill-transparent active:stroke-sky-400 hover:stroke-oli-400 pointer-events-auto"
        style={close ? "stroke-width: 2px;" : ""}
        marker-end="url(#arrow_path)"
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
    class="h-6 w-fit z-[9999] bg-oli rounded-lg absolute flex drop-shadow-md border border-oli-200 dark:border-oli-200"
    style="top: {edge_toolbar_pos.y}px; left: {edge_toolbar_pos.x}px; transform: translate(-50%, -50%);"
    on:mouseleave={() => (show_edge_toolbar = false)}
  >
    <svg
      class="bg-oli hover:bg-oli-100 active:bg-purple-200 rounded-lg cursor-pointer"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      ><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g
        id="SVGRepo_tracerCarrier"
        stroke-linecap="round"
        stroke-linejoin="round"
      ></g><g id="SVGRepo_iconCarrier">
        <path
          d="M6.46967 17.5303C6.17678 17.2374 6.17678 16.7626 6.46967 16.4697L8.68934 14.25H7.5C7.08579 14.25 6.75 13.9142 6.75 13.5C6.75 13.0858 7.08579 12.75 7.5 12.75H10.5C10.9142 12.75 11.25 13.0858 11.25 13.5V16.5C11.25 16.9142 10.9142 17.25 10.5 17.25C10.0858 17.25 9.75 16.9142 9.75 16.5V15.3107L7.53033 17.5303C7.23744 17.8232 6.76256 17.8232 6.46967 17.5303Z"
          fill="#1C274C"
        ></path>
        <path
          d="M16.5 11.25C16.9142 11.25 17.25 10.9142 17.25 10.5C17.25 10.0858 16.9142 9.75 16.5 9.75H15.3107L17.5303 7.53033C17.8232 7.23744 17.8232 6.76256 17.5303 6.46967C17.2374 6.17678 16.7626 6.17678 16.4697 6.46967L14.25 8.68934V7.5C14.25 7.08579 13.9142 6.75 13.5 6.75C13.0858 6.75 12.75 7.08579 12.75 7.5V10.5C12.75 10.9142 13.0858 11.25 13.5 11.25H16.5Z"
          fill="#1C274C"
        ></path>
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M11.9426 1.25H12.0574C14.3658 1.24999 16.1748 1.24998 17.5863 1.43975C19.031 1.63399 20.1711 2.03933 21.0659 2.93414C21.9607 3.82895 22.366 4.96897 22.5603 6.41371C22.75 7.82519 22.75 9.63423 22.75 11.9426V12.0574C22.75 14.3658 22.75 16.1748 22.5603 17.5863C22.366 19.031 21.9607 20.1711 21.0659 21.0659C20.1711 21.9607 19.031 22.366 17.5863 22.5603C16.1748 22.75 14.3658 22.75 12.0574 22.75H11.9426C9.63423 22.75 7.82519 22.75 6.41371 22.5603C4.96897 22.366 3.82895 21.9607 2.93414 21.0659C2.03933 20.1711 1.63399 19.031 1.43975 17.5863C1.24998 16.1748 1.24999 14.3658 1.25 12.0574V11.9426C1.24999 9.63423 1.24998 7.82519 1.43975 6.41371C1.63399 4.96897 2.03933 3.82895 2.93414 2.93414C3.82895 2.03933 4.96897 1.63399 6.41371 1.43975C7.82519 1.24998 9.63423 1.24999 11.9426 1.25ZM6.61358 2.92637C5.33517 3.09825 4.56445 3.42514 3.9948 3.9948C3.42514 4.56445 3.09825 5.33517 2.92637 6.61358C2.75159 7.91356 2.75 9.62178 2.75 12C2.75 14.3782 2.75159 16.0864 2.92637 17.3864C3.09825 18.6648 3.42514 19.4355 3.9948 20.0052C4.56445 20.5749 5.33517 20.9018 6.61358 21.0736C7.91356 21.2484 9.62178 21.25 12 21.25C14.3782 21.25 16.0864 21.2484 17.3864 21.0736C18.6648 20.9018 19.4355 20.5749 20.0052 20.0052C20.5749 19.4355 20.9018 18.6648 21.0736 17.3864C21.2484 16.0864 21.25 14.3782 21.25 12C21.25 9.62178 21.2484 7.91356 21.0736 6.61358C20.9018 5.33517 20.5749 4.56445 20.0052 3.9948C19.4355 3.42514 18.6648 3.09825 17.3864 2.92637C16.0864 2.75159 14.3782 2.75 12 2.75C9.62178 2.75 7.91356 2.75159 6.61358 2.92637Z"
          fill="#1C274C"
        ></path>
      </g></svg
    >
    <svg
      class="bg-oli hover:bg-oli-100 active:bg-red-200 rounded-lg cursor-pointer"
      viewBox="0 0 24 24"
      fill="none"
      on:click={delete_edge}
      on:keydown={delete_edge}
      xmlns="http://www.w3.org/2000/svg"
      ><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g
        id="SVGRepo_tracerCarrier"
        stroke-linecap="round"
        stroke-linejoin="round"
      ></g><g id="SVGRepo_iconCarrier">
        <path
          d="M10.0303 8.96967C9.73741 8.67678 9.26253 8.67678 8.96964 8.96967C8.67675 9.26256 8.67675 9.73744 8.96964 10.0303L10.9393 12L8.96966 13.9697C8.67677 14.2626 8.67677 14.7374 8.96966 15.0303C9.26255 15.3232 9.73743 15.3232 10.0303 15.0303L12 13.0607L13.9696 15.0303C14.2625 15.3232 14.7374 15.3232 15.0303 15.0303C15.3232 14.7374 15.3232 14.2625 15.0303 13.9697L13.0606 12L15.0303 10.0303C15.3232 9.73746 15.3232 9.26258 15.0303 8.96969C14.7374 8.6768 14.2625 8.6768 13.9696 8.96969L12 10.9394L10.0303 8.96967Z"
          fill="#1C274C"
        ></path>
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M12.0574 1.25H11.9426C9.63424 1.24999 7.82519 1.24998 6.41371 1.43975C4.96897 1.63399 3.82895 2.03933 2.93414 2.93414C2.03933 3.82895 1.63399 4.96897 1.43975 6.41371C1.24998 7.82519 1.24999 9.63422 1.25 11.9426V12.0574C1.24999 14.3658 1.24998 16.1748 1.43975 17.5863C1.63399 19.031 2.03933 20.1711 2.93414 21.0659C3.82895 21.9607 4.96897 22.366 6.41371 22.5603C7.82519 22.75 9.63423 22.75 11.9426 22.75H12.0574C14.3658 22.75 16.1748 22.75 17.5863 22.5603C19.031 22.366 20.1711 21.9607 21.0659 21.0659C21.9607 20.1711 22.366 19.031 22.5603 17.5863C22.75 16.1748 22.75 14.3658 22.75 12.0574V11.9426C22.75 9.63423 22.75 7.82519 22.5603 6.41371C22.366 4.96897 21.9607 3.82895 21.0659 2.93414C20.1711 2.03933 19.031 1.63399 17.5863 1.43975C16.1748 1.24998 14.3658 1.24999 12.0574 1.25ZM3.9948 3.9948C4.56445 3.42514 5.33517 3.09825 6.61358 2.92637C7.91356 2.75159 9.62177 2.75 12 2.75C14.3782 2.75 16.0864 2.75159 17.3864 2.92637C18.6648 3.09825 19.4355 3.42514 20.0052 3.9948C20.5749 4.56445 20.9018 5.33517 21.0736 6.61358C21.2484 7.91356 21.25 9.62177 21.25 12C21.25 14.3782 21.2484 16.0864 21.0736 17.3864C20.9018 18.6648 20.5749 19.4355 20.0052 20.0052C19.4355 20.5749 18.6648 20.9018 17.3864 21.0736C16.0864 21.2484 14.3782 21.25 12 21.25C9.62177 21.25 7.91356 21.2484 6.61358 21.0736C5.33517 20.9018 4.56445 20.5749 3.9948 20.0052C3.42514 19.4355 3.09825 18.6648 2.92637 17.3864C2.75159 16.0864 2.75 14.3782 2.75 12C2.75 9.62177 2.75159 7.91356 2.92637 6.61358C3.09825 5.33517 3.42514 4.56445 3.9948 3.9948Z"
          fill="#1C274C"
        ></path>
      </g></svg
    >
  </div>
{/if}
