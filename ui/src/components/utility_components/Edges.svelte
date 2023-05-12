<script lang="ts">
    import { onMount } from "svelte";

    export let current_cell_id;
    export let next_id;

    import { cells, id_map } from "../../stores/notebook";
    import Markdown from "../cell_components/Icons/markdown.svelte";

    $: c = $cells[$id_map[current_cell_id]];
    $: n = $cells[$id_map[next_id]];

    onMount(() => {
        c = $cells[$id_map[current_cell_id]];
        n = $cells[$id_map[next_id]];
    });

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
    $: width =
        Math.abs(curr.left - next.left) + Math.max(curr.width, next.width);
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

    $: anchor_dis = Math.sqrt(
        Math.pow(_curr_anchor.x - _next_anchor.x, 2) +
            Math.pow(_curr_anchor.y - _next_anchor.y, 2)
    );

    // straight line or curve (if distance is too large)
    let path = "";
    $: close =
        curr.right > next.left &&
        curr.left < next.right &&
        next.top - curr.bottom < 20;

    $: path = `M ${_curr_anchor.x} ${_curr_anchor.y}
                C ${_curr_anchor.x} ${_curr_anchor.y + 50}, 
                ${_next_anchor.x} ${_next_anchor.y - 50}, 
                ${_next_anchor.x} ${_next_anchor.y - 3}`;
</script>

<div
    class="bg-transparent"
    id="edge"
    style="
    position: absolute; 
    top: {top}px; left: {left}px; 
    width: {width}px; height: {height}px; 
    border-radius: 0.25rem; 
    pointer-events: none;"
>
    <svg
        height="100%"
        width="100%"
        style="position: absolute; top: 0; left: 0;"
    >
        <defs>
            <marker
                id="arrow_path"
                viewBox="0 -5 10 10"
                refX="5"
                refY="0"
                markerWidth="4"
                markerHeight="4"
                orient="auto"
                class="fill-neutral-500"
            >
                <path d="M0,-5L10,0L0,5" />
            </marker>
            <marker
                id="arrow_line"
                viewBox="0 -5 10 10"
                refX="5"
                refY="0"
                markerWidth="4"
                markerHeight="4"
                orient="auto"
                class="fill-neutral-500/30"
            >
                <path d="M0,-5L10,0L0,5" />
            </marker>
        </defs>
        <!-- downward facing arrow -->
        {#if !close}
            <path
                d={path}
                class="stroke-neutral-500 stroke-[2px] fill-transparent"
                style={close ? "stroke-width: 2px;" : ""}
                marker-end="url(#arrow_path)"
            />
        {:else}
            <line
                x1={_curr_anchor.x}
                y1={_curr_anchor.y}
                x2={_next_anchor.x}
                y2={_next_anchor.y}
                class="stroke-neutral-500 stroke-[2px]"
                stroke-dasharray="5,5"
                stroke-opacity="0.5"
                marker-end="url(#arrow_line)"
            />
        {/if}
        <!-- <svg
            x={_next_anchor.x - 6}
            y={_next_anchor.y - 6}
            width="12"
            height="12"
            viewBox="0 0 16 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            opacity={close ? 0.5 : 1}
        >
            <path
                d="M 8 8 L 15 0 H 0 L 8 8 Z"
                fill="currentColor"
                class="fill-neutral-500 hover:fill-neutral-700"
            />
        </svg> -->
    </svg>
</div>
