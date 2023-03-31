<script lang="ts">
    import { cells, id_map } from "../../stores/notebook";
    export let current_cell_id;
    export let next_id;

    $: current_cell_bottom =
        $cells[$id_map[current_cell_id]].metadata.gm.top +
        $cells[$id_map[current_cell_id]].metadata.gm.height;
    $: current_cell_bottom_mid =
        $cells[$id_map[current_cell_id]].metadata.gm.left +
        $cells[$id_map[current_cell_id]].metadata.gm.width / 2;
    $: current_cell_left = $cells[$id_map[current_cell_id]].metadata.gm.left;
    $: current_cell_right =
        $cells[$id_map[current_cell_id]].metadata.gm.left +
        $cells[$id_map[current_cell_id]].metadata.gm.width;

    $: next_cell_top = $cells[$id_map[next_id]].metadata.gm.top;
    $: next_cell_top_mid =
        $cells[$id_map[next_id]].metadata.gm.left +
        $cells[$id_map[next_id]].metadata.gm.width / 2;
    $: next_cell_left = $cells[$id_map[next_id]].metadata.gm.left;

    let x1, y1, x2, y2;
    let is_right = false;

    $: if (
        next_cell_top > current_cell_bottom &&
        next_cell_left < current_cell_right
    ) {
        x1 = current_cell_bottom_mid;
        y1 = current_cell_bottom;
        x2 = next_cell_top_mid;
        y2 = next_cell_top - 2;
        is_right = false;
    } else {
        x1 =
            $cells[$id_map[current_cell_id]].metadata.gm.left +
            $cells[$id_map[current_cell_id]].metadata.gm.width;
        y1 =
            $cells[$id_map[current_cell_id]].metadata.gm.top +
            $cells[$id_map[current_cell_id]].metadata.gm.height / 2;
        x2 = $cells[$id_map[next_id]].metadata.gm.left;
        y2 =
            $cells[$id_map[next_id]].metadata.gm.top +
            $cells[$id_map[next_id]].metadata.gm.height / 2;
        is_right = true;
    }

    $: mid_distance = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
    $: left_distance = Math.sqrt(
        (current_cell_bottom - next_cell_top) ** 2 +
            ($cells[$id_map[current_cell_id]].metadata.gm.left -
                $cells[$id_map[next_id]].metadata.gm.left) **
                2
    ); // left bottom corner of current cell to left top corner of next cell

    $: min_width = Math.min(
        $cells[$id_map[current_cell_id]].metadata.gm.width,
        $cells[$id_map[next_id]].metadata.gm.width
    );
</script>

<svg
    style="position: absolute; z-index: -1; pointer-events: none;"
    width="100%"
    height="100%"
    class="edge"
>
    {#if mid_distance > 20 && left_distance > 10}
        <!-- circle at start -->
        <circle cx={x1} cy={y1} r="2" class="circle" />
        {#if !is_right}
            <!-- bezier curve -->
            <path
                class="line"
                d={`M ${x1} ${y1} C ${x1} ${y1 + 50}, ${x2} ${y2 - 50}, ${x2} ${
                    y2 - 5
                }`}
            />
            <!-- downward facing arrow -->
            <path
                class="arrow"
                d={`M ${x2} ${y2} L ${x2 - 3} ${y2 - 5} L ${x2 + 3} ${
                    y2 - 5
                } Z`}
            />
        {:else}
            <!-- bezier curve -->
            <path
                class="line"
                d={`M ${x1} ${y1} C ${x1} ${y1}, ${x2 - 50} ${y2}, ${x2} ${y2}`}
            />
            <!-- right facing arrow -->
            <path
                class="arrow"
                d={`M ${x2} ${y2} L ${x2 - 5} ${y2 - 3} L ${x2 - 5} ${
                    y2 + 3
                } Z`}
            />
        {/if}
    {:else if y2 - y1 - 4 > 0}
        <!-- gradient  -->
        <defs>
            <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#00000044" />
                <stop offset="50%" stop-color="#77777744" />
                <stop offset="100%" stop-color="#ffffff44" />
            </linearGradient>
        </defs>
        <rect
            x={current_cell_left + 2}
            y={current_cell_bottom}
            width={min_width}
            height={y2 - y1 - 4}
            fill="url(#gradient)"
            style="stroke-width: 0;"
            rx="2"
            ry="2"
        />
    {/if}
</svg>

<style>
    .edge {
        stroke: #606060;
    }
    .circle {
        stroke-width: 3;
    }
    .line {
        stroke-width: 1;
        fill: none;
        pointer-events: all;
    }
    .line:hover {
        stroke-width: 2;
    }
    .arrow {
        stroke-width: 2;
        fill: #606060;
    }

    /* dark mode */
    @media (prefers-color-scheme: dark) {
        .edge {
            stroke: #d7d7d7;
        }
        .arrow {
            fill: #d7d7d7;
        }
    }
</style>
