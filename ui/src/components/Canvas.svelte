<script>
  import Notebook from "./Notebook.svelte";
  import { socket, open_socket, send_message } from "../stores/socket";
  import { onMount } from "svelte";
  let canvas_div = null;

  // middle mouse to pan
  import mouse_pos from "../stores/mouse.js";

  let moving = false;
  let clicked_x = 0;
  let clicked_y = 0;
  let mouseDown = function (e) {
    if (
      e.button === 0 && // if middle mouse button is pressed
      (e.target.id === "tissue" || e.target.id === "canvas")
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

  //// add event listeners
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

  let myContextMenu = null;
  let menu_left = 0;
  let menu_top = 0;
  function showCustomContextMenu(event) {
    event.preventDefault();
    menu_left = event.clientX;
    menu_top = event.clientY;
    myContextMenu.style.display = "block";
    // TODO: display to none if click outside or on menu
    // TODO: context menu on what is being clicked
  }
  document.addEventListener("contextmenu", showCustomContextMenu);
  document.addEventListener("click", () => {
    myContextMenu.style.display = "none";
  });
  document.addEventListener("scroll", () => {
    myContextMenu.style.display = "none";
  });
  document.addEventListener("wheel", () => {
    myContextMenu.style.display = "none";
  });

  // import ZoomToolBar from "../components/canvas_components/zoom.svelte";
  import ToolbarCanvas from "./canvas_components/ToolbarCanvas.svelte";
</script>

<div
  class="canvas bg-oli dark:bg-[#1E1E1E] relative overflow-auto"
  style="
        height: 20000px; 
        width: 20000px; 
        transform: scale({$zoom}); 
        transform-origin: 0 0 ;
        background-image: radial-gradient(
            circle at 0px 0px,
            rgb(112, 112, 112) 000 1px,
            transparent 0
        );
        background-size: 15px 15px;
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
</div>

<!-- <ZoomToolBar /> -->
<ToolbarCanvas />

<div
  class="h-fit w-40 bg-oli dark:bg-[#1E1E1E] fixed rounded z-50 text-oli-600 dark:text-oli-400 border border-oli-500 dark:border-oli-600"
  id="customContextMenu"
  style="top: {menu_top}px; left: {menu_left}px; position: fixed;"
  bind:this={myContextMenu}
>
  <ul>
    <li>Option 1</li>
    <li>Option 2</li>
    <li>Option 3</li>
  </ul>
</div>
