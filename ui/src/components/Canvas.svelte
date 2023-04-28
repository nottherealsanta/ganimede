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
                // $zoom -= 0.01;
                $zoom -= Math.sign(e.deltaY) * 0.1;
                if ($zoom < 1) $zoom = 1;
                if ($zoom > 2) $zoom = 2;
                this.window.scrollTo(
                    $mouse_pos.x - e.clientX / $zoom + 5000 / $zoom,
                    $mouse_pos.y - e.clientY / $zoom + 5000 / $zoom
                );
            }
            _log(e, "wheel");
        },
        { passive: false }
    );

    // $: this.window.scrollTo(e.pageX - e.clientX, e.pageY - e.clientY);

    function _log(e, x) {
        console.log(x);
        console.log($zoom);
        //log event

        console.log("page: ", e.pageX, e.pageY);
        console.log("client: ", e.clientX, e.clientY);
        console.log("scroll: ", window.scrollX, window.scrollY);
        console.log("mouse: ", $mouse_pos.x, $mouse_pos.y);
        console.log();
    }

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
        _log(e, "move");
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
