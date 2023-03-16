<script lang="ts">
    import { cells, id_map } from "../../stores/notebook";
    export let current_cell_id;
    export let next_id;

    $: x1 =
        $cells[$id_map[current_cell_id]].metadata.gm.left +
        $cells[$id_map[current_cell_id]].metadata.gm.width / 2;
    $: y1 =
        $cells[$id_map[current_cell_id]].metadata.gm.top +
        $cells[$id_map[current_cell_id]].metadata.gm.height;
    $: x2 =
        $cells[$id_map[next_id]].metadata.gm.left +
        $cells[$id_map[next_id]].metadata.gm.width / 2;
    $: y2 = $cells[$id_map[next_id]].metadata.gm.top;
</script>

<svg
    style="position: absolute; z-index: -1; pointer-events: none;"
    width="100%"
    height="100%"
>
    <path
        d={`M ${x1} ${y1} C ${x1} ${y1 + 50}, ${x2} ${y2 - 50}, ${x2} ${y2}`}
        stroke="black"
        stroke-width="2"
        fill="none"
    />
</svg>
