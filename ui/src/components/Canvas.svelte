<script>
    import Notebook from "./Notebook.svelte";
    import { zoom } from "../stores/zoom";
    import { socket, open_socket, send_message } from "../stores/socket";
    import { onMount } from "svelte";

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

    onMount(() => {
        open_socket();
    });
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
    {#await open_socket}
        <div>Waiting for socket</div>
    {:then}
        <Notebook />
    {/await}
</div>

<style>
    .canvas {
        position: relative;
        background-color: rgb(255, 255, 255);
        background-image: radial-gradient(
            circle at 0px 0px,
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
                circle at 0px 0px,
                rgb(129, 132, 136) 1px,
                transparent 0%
            );
        }
    }
</style>
