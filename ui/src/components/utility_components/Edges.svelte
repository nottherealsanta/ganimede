<script lang="ts">
    import { cells, id_map } from "../../stores/notebook";
    export let current_cell_id;
    export let next_id;

    $: current_cell_bottom =
        $cells[$id_map[current_cell_id]].top +
        $cells[$id_map[current_cell_id]].height;
    $: current_cell_bottom_mid =
        $cells[$id_map[current_cell_id]].left +
        $cells[$id_map[current_cell_id]].width / 2;
    $: current_cell_left = $cells[$id_map[current_cell_id]].left;
    $: current_cell_right =
        $cells[$id_map[current_cell_id]].left +
        $cells[$id_map[current_cell_id]].width;

    $: next_cell_top = $cells[$id_map[next_id]].top;
    $: next_cell_top_mid =
        $cells[$id_map[next_id]].left + $cells[$id_map[next_id]].width / 2;
    $: next_cell_left = $cells[$id_map[next_id]].left;

    let x1, y1, x2, y2;
    let is_right = false;

    $: if (
        next_cell_top > current_cell_bottom &&
        next_cell_left < current_cell_right
    ) {
        x1 = current_cell_bottom_mid;
        y1 = current_cell_bottom;
        x2 = next_cell_top_mid;
        y2 = next_cell_top;
        is_right = false;
    } else {
        x1 =
            $cells[$id_map[current_cell_id]].left +
            $cells[$id_map[current_cell_id]].width;
        y1 =
            $cells[$id_map[current_cell_id]].top +
            $cells[$id_map[current_cell_id]].height / 2;
        x2 = $cells[$id_map[next_id]].left;
        y2 = $cells[$id_map[next_id]].top + $cells[$id_map[next_id]].height / 2;
        is_right = true;
    }

    $: mid_distance = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
    $: x_distance = Math.sqrt(
        (current_cell_bottom - next_cell_top) ** 2 +
            ($cells[$id_map[current_cell_id]].left -
                $cells[$id_map[next_id]].left) **
                2
    );
    $: y_distance = Math.sqrt(
        (current_cell_bottom - next_cell_top) ** 2 +
            ($cells[$id_map[current_cell_id]].left -
                $cells[$id_map[next_id]].left) **
                2
    );
</script>

<svg
    style="position: absolute; pointer-events: none;"
    width="100%"
    height="100%"
    class="stroke-neutral-500 dark:stroke-neutral-400"
>
    {#if mid_distance > 35 && x_distance > 35}
        {#if !is_right}
            <!-- bezier curve -->
            <path
                class="stroke-1 fill-none pointer-events-all hover:stroke-2"
                d={`M ${x1} ${y1 + 1} C ${x1} ${y1 + 50}, ${x2} ${
                    y2 - 50
                }, ${x2} ${y2 - 5}`}
            />
            <!-- downward facing arrow -->
            <path
                class="stroke-2 fill-neutral-500 dark:fill-neutral-400"
                d={`M ${x2} ${y2 - 1} L ${x2 - 3} ${y2 - 5} L ${x2 + 3} ${
                    y2 - 5
                } Z`}
            />
        {:else}
            <!-- bezier curve -->
            <path
                class="stroke-1 fill-none pointer-events-all hover:stroke-2"
                d={`M ${x1} ${y1} C ${x1 + 50} ${y1}, ${
                    x2 - 50
                } ${y2}, ${x2} ${y2}`}
            />
            <!-- right facing arrow -->
            <path
                class="stroke-2 fill-neutral-500 dark:fill-neutral-400"
                d={`M ${x2} ${y2} L ${x2 - 5} ${y2 - 3} L ${x2 - 5} ${
                    y2 + 3
                } Z`}
            />
        {/if}
    {:else if y_distance < 35}
        <line
            class=" fill-none pointer-events-all"
            x1={current_cell_left + 25}
            y1={current_cell_bottom}
            x2={next_cell_left + 25}
            y2={next_cell_top}
            stroke-linecap="round"
            stroke-width="3"
        />
    {/if}
</svg>
