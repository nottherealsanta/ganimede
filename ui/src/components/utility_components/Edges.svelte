<script lang="ts">
    import { cells, id_map } from "../../stores/notebook";
    export let current_cell_id;
    export let next_id;

    $: current_cell_bottom =
        $cells[$id_map[current_cell_id]].metadata.gm.top +
        $cells[$id_map[current_cell_id]].metadata.gm.height;
    $: next_cell_top = $cells[$id_map[next_id]].metadata.gm.top;
    let x1, y1, x2, y2;
    let is_right = false;
    $: if (next_cell_top > current_cell_bottom) {
        x1 =
            $cells[$id_map[current_cell_id]].metadata.gm.left +
            $cells[$id_map[current_cell_id]].metadata.gm.width / 2;
        y1 =
            $cells[$id_map[current_cell_id]].metadata.gm.top +
            $cells[$id_map[current_cell_id]].metadata.gm.height;
        x2 =
            $cells[$id_map[next_id]].metadata.gm.left +
            $cells[$id_map[next_id]].metadata.gm.width / 2;
        y2 = $cells[$id_map[next_id]].metadata.gm.top - 2;
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

    $: distance = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
</script>

<svg
    style="position: absolute; z-index: -1; pointer-events: none;"
    width="100%"
    height="100%"
    class="edge"
>
    {#if distance > 50}
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
    {:else}
        <path class="line" d="M{x1} {y1} L{x2} {y2}" />
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
