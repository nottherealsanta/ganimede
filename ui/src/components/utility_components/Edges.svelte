<script lang="ts">
    export let current_cell_id;
    export let next_id;

    import { cells, id_map } from "../../stores/notebook";

    $: c = $cells[$id_map[current_cell_id]];
    $: n = $cells[$id_map[next_id]];

    function get_box(x) {
        return {
            left: x.left,
            right: x.left + x.width,
            top: x.top,
            bottom: x.top + x.height,
            center: {
                x: x.left + x.width / 2,
                y: x.top + x.height / 2,
            },
            width: x.width,
            height: x.height,
        };
    }

    $: curr = get_box(c);
    $: next = get_box(n);

    $: curr_anchor = {
        x: curr.center.x,
        y: curr.bottom,
    };
    $: next_anchor = {
        x: next.center.x,
        y: next.top,
    };

    $: top = curr_anchor.y > next_anchor.y ? next_anchor.y : curr_anchor.y;
    $: left = curr.left > next.left ? next.left : curr.left;
    $: width = Math.abs(curr.left - next.left) + curr.width;
    $: height = Math.abs(curr_anchor.y - next_anchor.y);

    // $: next_top_over_curr = next_anchor.y < curr_anchor.y;
    $: if (next_anchor.y - 50 < curr_anchor.y) {
        top -= 25;
        height += 50;
    }

    $: _curr_anchor = {
        x: curr_anchor.x - left,
        y: curr_anchor.y - top,
    };
    $: _next_anchor = {
        x: next_anchor.x - left,
        y: next_anchor.y - top,
    };

    $: path = `M ${_curr_anchor.x} ${_curr_anchor.y} C ${_curr_anchor.x} ${
        _curr_anchor.y + 50
    }, ${_next_anchor.x} ${_next_anchor.y - 50}, ${_next_anchor.x} ${
        _next_anchor.y
    }`;
</script>

<div
    class="bg-transparent"
    style="
    position: absolute; 
    top: {top}px; left: {left}px; 
    width: {width}px; height: {height}px; 
    z-index: -1; border-radius: 0.25rem; 
    pointer-events: none;"
>
    <svg
        height="100%"
        width="100%"
        style="position: absolute; top: 0; left: 0; z-index: -1; pointer-events: all;"
    >
        <path
            d={path}
            class="stroke-neutral-500 hover:stroke-neutral-700 stroke-1 fill-transparent"
        />
        <!-- downward facing arrow -->
        <path
            d={`M ${_next_anchor.x} ${_next_anchor.y} L ${_next_anchor.x + 4} ${
                _next_anchor.y - 8
            } L ${_next_anchor.x - 4} ${_next_anchor.y - 8} z`}
            class="fill-neutral-500 hover:fill-neutral-700"
        />
    </svg>
</div>
