<script>
    import Cell from "./Cell.svelte";
    import Edges from "./utility_components/Edges.svelte";
    import { dndzone } from "svelte-dnd-action";

    import {
        cells,
        id_map,
        pc_graph,
        cp_graph,
        np_graph,
        parent_less_cells,
        heading_levels_inv,
        notebook,
    } from "../stores/notebook";
    import Tissue from "./Tissue.svelte";

    function align_parent_less_cells() {
        if (
            $parent_less_cells.length > 0 &&
            $parent_less_cells.every((cell_id) => {
                return (
                    $cells[$id_map[cell_id]].top === 0 &&
                    $cells[$id_map[cell_id]].left === 0
                );
            })
        ) {
            let top = 5000;
            let left = 5000;
            for (let cell_id of $parent_less_cells) {
                $cells[$id_map[cell_id]].top = top;
                top += $cells[$id_map[cell_id]].height + 10;
                $cells[$id_map[cell_id]].left = left;
            }
        }
        window.scrollTo(4500, 4800);
    }

    // wait for $cell to be defined
    let aligned = false;
    $: if ($cells !== undefined && !aligned) {
        // align_parent_less_cells();
        aligned = true;
        // call align_parent_less_cells() after 1 second
        setTimeout(align_parent_less_cells, 1000);
    }

    function topological_sort(digraph) {
        // digraph is a dictionary:
        //   key: a node
        // value: a set of adjacent neighboring nodes

        // construct a dictionary mapping nodes to their
        // indegrees
        let indegrees = {};
        for (let node in digraph) {
            indegrees[node] = 0;
        }
        for (let node in digraph) {
            for (let neighbor of digraph[node]) {
                indegrees[neighbor] += 1;
            }
        }

        // track nodes with no incoming edges
        let nodes_with_no_incoming_edges = [];
        for (let node in digraph) {
            if (indegrees[node] === 0) {
                nodes_with_no_incoming_edges.push(node);
            }
        }

        // initially, no nodes in our ordering
        let topological_ordering = [];

        // as long as there are nodes with no incoming edges
        // that can be added to the ordering
        while (nodes_with_no_incoming_edges.length > 0) {
            // add one of those nodes to the ordering
            let node = nodes_with_no_incoming_edges.pop();
            topological_ordering.push(node);

            // decrement the indegree of that node's neighbors
            for (let neighbor of digraph[node]) {
                indegrees[neighbor] -= 1;
                if (indegrees[neighbor] === 0) {
                    nodes_with_no_incoming_edges.push(neighbor);
                }
            }
        }

        // we've run out of nodes with no incoming edges
        // did we add all the nodes or find a cycle?
        if (topological_ordering.length === Object.keys(digraph).length) {
            return topological_ordering; // got them all
        } else {
            throw new Error(
                "Graph has a cycle! No topological ordering exists."
            );
        }
    }

    let pc_graph_topological_ordering = [];
    $: if ($pc_graph) {
        pc_graph_topological_ordering = topological_sort(
            JSON.parse(JSON.stringify($pc_graph))
        );
        // console.log(pc_graph_topological_ordering);
    }
</script>

{#if $cells !== undefined}
    <!-- {#each pc_graph_topological_ordering as cell_id}
        <Tissue {cell_id} />
    {/each} -->

    {#each $cells.map((cell) => cell.id) as cell_id}
        {#if !($cells[$id_map[cell_id]].type === "markdown" && cell_id in $pc_graph)}
            <Cell {cell_id} />
        {:else}
            <Tissue {cell_id} />
        {/if}
    {/each}
{/if}
