<script>
    import Notebook from "./Notebook.svelte";
    import { zoom } from "../stores/zoom";
    import { socket, open_socket, send_message } from "../stores/socket";
    import { onMount } from "svelte";
    let canvas_div = null;

    // zoom
    import mouse_pos from "../stores/mouse.js";

    let min_zoom = 0.3;
    let max_zoom = 1.7;
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
                        // let next_scroll_X =
                        //     window.scrollX -
                        //     $mouse_pos.x * d_zoom * Math.sign(e.deltaY);
                        // let next_scroll_Y =
                        //     window.scrollY -
                        //     $mouse_pos.y * d_zoom * Math.sign(e.deltaY);

                        // window.scrollTo(next_scroll_X, next_scroll_Y);
                        this.window.scrollBy({
                            left: -$mouse_pos.x * d_zoom * Math.sign(e.deltaY),
                            top: -$mouse_pos.y * d_zoom * Math.sign(e.deltaY),
                            behavior: "instant",
                        });
                    } else if ($zoom > max_zoom) {
                        $zoom = max_zoom;
                    }
                }
            }
        },
        { passive: false }
    );
    function increase_zoom() {
        $zoom += 0.1;
        $zoom = Math.round($zoom * 100) / 100;
        if ($zoom > max_zoom) {
            $zoom = max_zoom;
        } else {
            window.scrollTo(window.scrollX + 500, window.scrollY + 100);
        }
    }

    function decrease_zoom() {
        $zoom -= 0.1;
        $zoom = Math.round($zoom * 100) / 100;
        if ($zoom < min_zoom) {
            $zoom = min_zoom;
        } else {
            window.scrollTo(window.scrollX - 500, window.scrollY - 100);
        }
    }

    // middle mouse to pan
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
            window.scrollTo(
                window.scrollX + clicked_x - $mouse_pos.x,
                window.scrollY + clicked_y - $mouse_pos.y
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

<div
    id="zoom"
    class="fixed flex flex-row bottom-5 w-[120px] h-8 right-5 p-[1px] bg-neutral-100 dark:bg-neutral-800
    border rounded border-neutral-300 dark:border-neutral-700 justify-center align-middle pointer-events-auto"
>
    <div
        id="decrease_zoom"
        class="font-bold px-0 cursor-pointer w-[35px] h-full flex justify-center items-center hover:bg-neutral-300/50"
        on:click={decrease_zoom}
        on:keydown={(e) => {}}
    >
        -
    </div>

    <div
        class="font-bold border-x-1 border-neutral-300 dark:border-neutral-700 p-0 flex justify-center items-center w-[50px]"
    >
        {Math.round($zoom * 100)}%
    </div>
    <div
        id="increase_zoom"
        class="font-bold px-0 cursor-pointer w-[35px] h-full flex justify-center items-center hover:bg-neutral-300/50"
        on:click={increase_zoom}
        on:keydown={(e) => {}}
    >
        +
    </div>
</div>
