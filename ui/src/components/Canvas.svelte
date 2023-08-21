<script>
  import Notebook from "./Notebook.svelte";
  import { socket, open_socket, send_message } from "../stores/socket";
  import { onMount } from "svelte";
  let canvas_div = null;

  // ---------- mouse click to pan
  import mouse_pos from "../stores/mouse.js";

  let moving = false;
  let clicked_x = 0;
  let clicked_y = 0;
  let mouseDown = function (e) {
    if (
      e.button === 0 && // if middle mouse button is pressed
      e.target.id === "canvas"
    ) {
      moving = true;
      clicked_x = $mouse_pos.x;
      clicked_y = $mouse_pos.y;
    }
  };
  let mouseUp = function () {
    moving = false;
  };
  let mouseMove = function (e) {
    if (moving) {
      window.scrollBy({
        left: clicked_x - $mouse_pos.x,
        top: clicked_y - $mouse_pos.y,
        behavior: "instant",
      });
    }
  };

  // ---------- zoom
  import { zoom, set_zoom } from "../stores/zoom";

  // add event listeners
  onMount(() => {
    window.addEventListener(
      "wheel",
      (event) => {
        set_zoom(event);
      },
      { passive: false },
    );
  });

  onMount(async () => {
    open_socket();
  });

  // ---------- context menu

  let right_click_menu = null;
  let menu_left = 0;
  let menu_top = 0;
  function showCustomContextMenu(event) {
    event.preventDefault();
    menu_left = event.clientX;
    menu_top = event.clientY;
    right_click_menu.style.display = "block";
    // TODO: display to none if click outside or on menu
    // TODO: context menu on what is being clicked
  }
  document.addEventListener("contextmenu", showCustomContextMenu);
  document.addEventListener("click", () => {
    if (right_click_menu) {
      right_click_menu.style.display = "none";
    }
  });
  document.addEventListener("scroll", () => {
    if (right_click_menu) {
      right_click_menu.style.display = "none";
    }
  });
  document.addEventListener("wheel", () => {
    if (right_click_menu) {
      right_click_menu.style.display = "none";
    }
  });

  // ---------- scroll
  // debug
  // let scroll_x = 0;
  // let scroll_y = 0;

  // let view_width = 0;
  // let view_height = 0;

  // document.addEventListener("scroll", () => {
  //   scroll_x = window.scrollX / $zoom;
  //   scroll_y = window.scrollY / $zoom;
  //   view_width = window.innerWidth / $zoom;
  //   view_height = window.innerHeight / $zoom;
  // });

  // $: center_x = scroll_x + view_width / 2;
  // $: center_y = scroll_y + view_height / 2;

  // ---------- toolbar
  import ToolbarCanvas from "./canvas_components/ToolbarCanvas.svelte";
  import Python from "./cell_components/Icons/python.svelte";
  import Markdown from "./cell_components/Icons/markdown.svelte";

  import { create_cell } from "../stores/_notebook";
</script>

<div
  class="canvas bg-oli dark:bg-[#1E1E1E] relative overflow-auto"
  style="
        height: 20000px; 
        width: 20000px; 
        transform: scale({$zoom}); 
        transform-origin: 0 0;
        background-image: radial-gradient(
            circle at 0px 0px,
            rgb(112, 112, 112) 000 1px,
            transparent 0
        );
        background-size: 25px 25px;
    "
  id="canvas"
  on:mousemove={mouseMove}
  on:mousedown={mouseDown}
  on:mouseup={mouseUp}
  bind:this={canvas_div}
>
  {#await open_socket}
    <div>Waiting for socket</div>
  {:then}
    <Notebook />
  {/await}

  <!-- debug -->

  <!-- <div
    class="h-5 w-5"
    style="top: {$mouse_pos.y +
      10}px; left: {$mouse_pos.x}px; position: absolute;"
  >
    {$mouse_pos.x}, {$mouse_pos.y}
  </div> -->
  <!-- <div
    class="bg-sky-100/10"
    style="top: {scroll_y}px; left: {scroll_x}px; position: absolute; width: {window.innerWidth /
      $zoom}px; height: {window.innerHeight / $zoom}px;"
  ></div>
  <div
    class="w-1 h-1 bg-red-400"
    style="top: {center_y}px; left: {center_x}px; position: absolute;"
  ></div> -->
</div>

<!-- <ZoomToolBar /> -->
<ToolbarCanvas />

<div
  class="h-fit w-100 bg-oli py-0.5 px-0.5 dark:bg-[#1E1E1E] font-['Roboto_Mono'] fixed rounded z-50 border border-oli-200 dark:border-oli-600 stroke-none"
  id="customContextMenu"
  style="top: {menu_top}px; left: {menu_left}px; position: fixed; display: none;"
  bind:this={right_click_menu}
>
  <ul>
    <li>
      <button
        class="h-7 px-2 py-1 m-0 flex flex-row bg-transparent border-none hover:bg-oli-100/50 items-center justify-center cursor-pointer fill-oli-400 hover:fill-oli-500 dark:hover:fill-oli-300 text-oli-400 hover:text-oli-500 dark:hover:text-oli-300"
        on:click={create_cell(
          "code",
          null,
          $mouse_pos.x - 50,
          $mouse_pos.y - 15,
        )}
      >
        <div class="w-5 mr-1"><Python /></div>
        Code Cell
      </button>
    </li>
    <li>
      <button
        class="h-7 px-2 py-1 m-0 flex flex-row bg-transparent border-none hover:bg-oli-100/50 items-center justify-center cursor-pointer fill-oli-400 hover:fill-oli-500 dark:hover:fill-oli-300 text-oli-400 hover:text-oli-500 dark:hover:text-oli-300"
        on:click={create_cell(
          "markdown",
          null,
          $mouse_pos.x - 50,
          $mouse_pos.y - 15,
        )}
      >
        <div class="w-5 mr-1"><Markdown /></div>
        Text Cell
      </button>
    </li>
  </ul>
</div>
