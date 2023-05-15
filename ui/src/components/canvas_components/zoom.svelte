<script>
    import { zoom } from "../../stores/zoom.js";
    import mouse_pos from "../../stores/mouse.js";

    let min_zoom = 0.6;
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
    function zoom_in() {
        $zoom += 0.1;
        $zoom = Math.round($zoom * 100) / 100;
        if ($zoom > max_zoom) {
            $zoom = max_zoom;
        } else {
            window.scrollTo(window.scrollX + 500, window.scrollY + 100);
        }
    }

    function zoom_out() {
        $zoom -= 0.1;
        $zoom = Math.round($zoom * 100) / 100;
        if ($zoom < min_zoom) {
            $zoom = min_zoom;
        } else {
            window.scrollTo(window.scrollX - 500, window.scrollY - 100);
        }
    }
</script>

<div
    id="zoom"
    class="fixed flex flex-row bottom-5 w-[120px] h-8 left-5 p-[1px] bg-neutral-100 dark:bg-neutral-800 border rounded border-neutral-300 dark:border-neutral-700 justify-center align-middle pointer-events-auto"
>
    <div
        id="zoom_out"
        class="font-bold px-0 cursor-pointer w-[35px] h-full flex justify-center items-center hover:bg-neutral-300/50"
        on:click={zoom_out}
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
        id="zoom_in"
        class="font-bold px-0 cursor-pointer w-[35px] h-full flex justify-center items-center hover:bg-neutral-300/50"
        on:click={zoom_in}
        on:keydown={(e) => {}}
    >
        +
    </div>
</div>
