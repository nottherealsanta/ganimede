<script>
    export let left = 100;
    export let top = 100;

    let moving = false;

    function onMouseDown(e) {
        if (e.target.id == "draggable") {
            moving = true;
        }
    }

    function onMouseMove(e) {
        if (moving) {
            left += e.movementX;
            top += e.movementY;
        }
    }

    function onMouseUp() {
        moving = false;
    }
</script>

<section
    on:mousedown={onMouseDown}
    style="left: {left}px; top: {top}px;"
    class="draggable"
    id="draggable"
>
    <slot />
</section>

<svelte:window on:mouseup={onMouseUp} on:mousemove={onMouseMove} />

<style>
    .draggable {
        /* user-select: none; */
        cursor: grab;
        /* position: absolute; */
    }
    .draggable:active {
        cursor: grabbing;
    }
</style>
