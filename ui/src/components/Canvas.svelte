<script>
    import Notebook from "./Notebook.svelte";
    import { zoom } from "../stores/zoom";

    // zoom
    window.addEventListener(
        "wheel",
        function (e) {
            if (e.ctrlKey) {
                e.preventDefault();
                $zoom -= e.deltaY / 250;
                if ($zoom < 0.1) $zoom = 0.1;
                // this.document.body.style.zoom = $zoom;
            }
        },
        { passive: false }
    );
</script>

<div
    class="canvas"
    style="
        height: 10000px; 
        width: 10000px; 
        transform: scale({$zoom}); 
        transform-origin: 0 0;
    "
>
    <Notebook />
</div>

<style>
    .canvas {
        position: relative;
        background-color: rgb(255, 255, 255);
        background-image: radial-gradient(
            circle at 12.5px 12.5px,
            rgb(126, 123, 119) 000 1px,
            transparent 0
        );
        background-size: 25px 25px;
        overflow: scroll;
    }
    /* darkmode */
    @media (prefers-color-scheme: dark) {
        .canvas {
            background-color: rgb(39, 40, 43);
            background-image: radial-gradient(
                circle at 12.5px 12.5px,
                rgb(129, 132, 136) 1px,
                transparent 0%
            );
        }
    }
</style>
