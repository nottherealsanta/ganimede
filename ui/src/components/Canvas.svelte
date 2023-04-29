<script>
    import Notebook from "./Notebook.svelte";
    import { zoom } from "../stores/zoom";
    import { socket, open_socket, send_message } from "../stores/socket";
    import { onMount } from "svelte";
    let canvas_div = null;

    // zoom
    import mouse_pos from "../stores/mouse.js";

    let min_zoom = 0.5;
    let max_zoom = 3;
    let d_zoom = 0.1;

    window.addEventListener(
        "wheel",
        function (e) {
            if (e.ctrlKey) {
                e.preventDefault();
                e.stopImmediatePropagation();

                if ($mouse_pos.x !== 0 && $mouse_pos.y !== 0) {
                    // $zoom -= 0.01;
                    $zoom -= Math.sign(e.deltaY) * d_zoom;
                    $zoom = Math.round($zoom * 100) / 100;

                    if ($zoom < min_zoom) {
                        $zoom = min_zoom;
                    } else if ($zoom >= min_zoom && $zoom <= max_zoom) {
                        let next_scroll_X =
                            window.scrollX -
                            $mouse_pos.x * d_zoom * Math.sign(e.deltaY);
                        let next_scroll_Y =
                            window.scrollY -
                            $mouse_pos.y * d_zoom * Math.sign(e.deltaY);

                        window.scrollTo(next_scroll_X, next_scroll_Y);
                    } else if ($zoom > max_zoom) {
                        $zoom = max_zoom;
                    }
                }
            }
        },
        { passive: false }
    );

    // middle mouse to pan
    let moving = false;
    let clicked_x = 0;
    let clicked_y = 0;
    let mouseDown = function (e) {
        // if left click
        if (e.button === 1 && e.target.id === "canvas") {
            moving = true;
            clicked_x = e.offsetX;
            clicked_y = e.offsetY;
        }
    };
    let mouseUp = function () {
        moving = false;
    };
    let mouseMove = function (e) {
        if (moving) {
            window.scrollTo(
                window.scrollX + clicked_x - e.offsetX,
                window.scrollY + clicked_y - e.offsetY
            );
        }
    };

    onMount(() => {
        open_socket();
        // TODO: check config for user-saved view-x, view-y, view-$zoom
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
