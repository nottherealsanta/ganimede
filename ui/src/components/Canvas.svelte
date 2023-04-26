<script>
    import Notebook from "./Notebook.svelte";
    import { zoom } from "../stores/zoom";
    import { socket, open_socket, send_message } from "../stores/socket";
    import { onMount } from "svelte";
    let canvas_div = null;

    // zoom
    import mouse_pos from "../stores/mouse.js";

    window.addEventListener(
        "wheel",
        function (e) {
            if (e.ctrlKey) {
                e.preventDefault();
                $zoom -= e.deltaY / 250;
                if ($zoom < 0.1) $zoom = 0.1;
                if ($zoom > 10) $zoom = 10;
                this.window.scrollTo(
                    $mouse_pos.x - (e.clientX - e.target.offsetLeft),
                    $mouse_pos.y - (e.clientY - e.target.offsetTop)
                );
            }
        },
        { passive: false }
    );

    // middle mouse to pan
    let moving = false;
    let clicked_x = 0;
    let clicked_y = 0;
    let mouseDown = function (event) {
        // if left click
        if (event.button === 1 && event.target.id === "canvas") {
            moving = true;
            clicked_x = event.offsetX;
            clicked_y = event.offsetY;
        }
    };
    let mouseUp = function () {
        moving = false;
    };
    let mouseMove = function (event) {
        if (moving) {
            window.scrollTo(
                window.scrollX + clicked_x - event.offsetX,
                window.scrollY + clicked_y - event.offsetY
            );
        }
    };

    onMount(() => {
        open_socket();
        // TODO: check config for user-saved view-x, view-y, view-zoom
        // window.scrollTo(5000, 5000);
    });
</script>

<div
    class=" bg-zinc-100
     dark:bg-neutral-800
     relative overflow-auto
     "
    style="
        height: 10000px; 
        width: 10000px; 
        transform: scale({$zoom}); 
        transform-origin: 0 0;
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
