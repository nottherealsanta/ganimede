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

    // path
    $: if (next_anchor.y - 50 < curr_anchor.y) {
        top -= 25;
        height += 50;
    }

    // $: _curr_anchor = {
    //     x: curr_anchor.x - left,
    //     y: curr_anchor.y - top,
    // };
    // $: _next_anchor = {
    //     x: next_anchor.x - left,
    //     y: next_anchor.y - top,
    // };
    let path = "";
    $: path = `M ${curr.left + 32 - left} ${curr.bottom - top + 5}
                C ${curr.left + 32 - left} ${curr.bottom - top + 50}, 
                ${next.left + 25 - left} ${next.top - top - 50}, 
                ${next.left + 25 - left} ${next.top - top - 5}`;

    // straight line or curve (if distance is too large)
    // $: close =
    //     curr.right > next.left &&
    //     curr.left < next.right &&
    //     next.top - curr.bottom < 20;

    // use this logic instead
    // cell.top - (prev_cell.top + prev_cell.height) < 100 &&
    //                 cell.left - prev_cell.left < 50 &&
    //                 cell.left - prev_cell.left > -50

    $: close =
        next.top - curr.bottom < 100 &&
        next.left - curr.left < 50 &&
        next.left - curr.left > -50;

    // line should start from current bottom, current left + 25 and end at next top, next left + 25
    $: line = {
        x1: curr.left + 32 - left,
        y1: curr.bottom - top + 5,
        x2: next.left + 32 - left,
        y2: next.top - top - 5,
    };
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
        style="position: absolute; top: 0; left: 0; "
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
                class="fill-oli-300 dark:fill-oli-200"
            >
                <path d="M0,-5L10,0L0,5" />
            </marker>
            <marker
                id="arrow_line"
                viewBox="0 -5 10 10"
                refX="5"
                refY="0"
                markerWidth="3"
                markerHeight="3"
                orient="auto"
                class="fill-oli-400/30 dark:fill-oli-200/30"
            >
                <path d="M0,-5L10,0L0,5" />
            </marker>
            <marker
                id="circle_marker"
                viewBox="0 0 10 10"
                refX="5"
                refY="5"
                markerWidth="5"
                markerHeight="5"
                orient="auto"
                class="fill-oli-400/30 dark:fill-oli-200/30"
            >
                <circle cx="5" cy="5" r="3" />
            </marker>
        </defs>
        <!-- downward facing arrow -->
        {#if !close}
            <path
                d={path}
                class="stroke-oli-300 stroke-[2px] fill-transparent hover:stroke-neutral-800 hover:dark:stroke-neutral-200"
                style={close ? "stroke-width: 2px;" : ""}
                marker-end="url(#arrow_path)"
            />
        {:else}
            <line
                x1={line.x1}
                y1={line.y1}
                x2={line.x2}
                y2={line.y2}
                class="stroke-neutral-500 stroke-[2px] fill-transparent hover:stroke-neutral-800 hover:dark:stroke-neutral-200"
                stroke-dasharray="5,5"
                stroke-opacity="0.5"
                marker-end="url(#arrow_line)"
            />
        {/if}
    </svg>
</div>
