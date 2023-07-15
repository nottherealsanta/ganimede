<script>
    import Notebook from "./Notebook.svelte";
    import { zoom } from "../stores/zoom";
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
            e.button === 1 && // if middle mouse button is pressed
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

    onMount(async () => {
        open_socket();
    });

    // import ZoomToolBar from "../components/canvas_components/zoom.svelte";
    import ToolbarCanvas from "./canvas_components/ToolbarCanvas.svelte";
</script>

<div
    class="canvas bg-oli dark:bg-oli-800 relative overflow-auto"
    style="
        height: 10000px; 
        width: 10000px; 
        transform: scale({$zoom}); 
        transform-origin: 0 0 ;
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
</div>

<!-- <ZoomToolBar /> -->
<ToolbarCanvas />
