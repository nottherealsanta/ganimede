<script lang="ts">
    import { cells, id_map } from "../../stores/notebook";
    export let current_cell_id;
    export let next_id;

    $: current_cell = $cells[$id_map[current_cell_id]];
    $: current_cell_bottom = current_cell.top + current_cell.height;
    $: current_cell_center = current_cell.left + current_cell.width / 2;
    $: current_cell_left = current_cell.left;
    $: current_cell_right = current_cell.left + current_cell.width;
    $: current_cell_mid = current_cell.top + current_cell.height / 2;

    $: next_cell = $cells[$id_map[next_id]];
    $: next_cell_top = next_cell.top;
    $: next_cell_center = next_cell.left + next_cell.width / 2;
    $: next_cell_left = next_cell.left;
    $: next_cell_mid = next_cell.top + next_cell.height / 2;

    let x1, y1, x2, y2;
    let is_right = false;

    $: if (
        next_cell_top > current_cell_bottom &&
        next_cell_left < current_cell_right
    ) {
        x1 = current_cell_center;
        y1 = current_cell_bottom;
        x2 = next_cell_center;
        y2 = next_cell_top;
        is_right = false;
    } else {
        x1 = current_cell_right;
        y1 = current_cell_mid;
        x2 = next_cell_left;
        y2 = next_cell_mid;
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
