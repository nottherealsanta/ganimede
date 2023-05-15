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
        // if left click
        if (
            e.button === 1 &&
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
            // window.scrollTo(
            //     window.scrollX + clicked_x - $mouse_pos.x,
            //     window.scrollY + clicked_y - $mouse_pos.y
            // );
            window.scrollBy({
                left: clicked_x - $mouse_pos.x,
                top: clicked_y - $mouse_pos.y,
                behavior: "instant",
            });
        }
    };

    // import Selecto from "svelte-selecto";

    onMount(() => {
        open_socket();
        // TODO: check config for user-saved view-x, view-y, view-$zoom
        // window.scrollTo(5000, 5000);
    });

    import ZoomToolBar from "../components/canvas_components/zoom.svelte";
</script>

<div
    class=" canvas bg-zinc-100
     dark:bg-neutral-800
     relative overflow-auto
     "
    style="
        height: 10000px; 
        width: 10000px; 
        transform: scale({$zoom}); 
        transform-origin: 0 0 ;
        background-image: radial-gradient(
            circle at 0px 0px,
            rgb(126, 123, 119) 000 1px,
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

<ZoomToolBar />
