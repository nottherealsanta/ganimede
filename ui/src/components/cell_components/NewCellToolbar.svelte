<script lang="ts">
    import { notebook, cells, id_map } from "../../stores/notebook";
    export let cell_id;

    async function new_code_cell() {
        const new_code_cell_response = await fetch("/notebook/new_cell", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                cell_type: "code",
                previous_cell_id: cell_id,
            }),
        });
        const data = await new_code_cell_response.json();
        const new_cell = data["new_cell"];
        const id_map = data["id_map"];

        new_cell["metadata"]["gm"]["previous"] = [cell_id];
        $cells[id_map[cell_id]]["metadata"]["gm"]["next"] = [
            ...$cells[id_map[cell_id]]["metadata"]["gm"]["next"],
            new_cell["id"],
        ];

        new_cell["metadata"]["gm"]["top"] =
            $cells[id_map[cell_id]]["metadata"]["gm"]["top"] +
            $cells[id_map[cell_id]]["metadata"]["gm"]["height"] +
            10;
        new_cell["metadata"]["gm"]["left"] =
            $cells[id_map[cell_id]]["metadata"]["gm"]["left"];

        $notebook["cells"] = [...$notebook["cells"], new_cell];
        $notebook["metadata"]["gm"]["id_map"] = id_map;

        console.log("new code cell");
        console.log($notebook);
    }

    function new_text_cell() {
        console.log("new text cell");
    }
</script>

<!-- on click console log -->
<div class="new-cell-toolbar">
    <button class="new-cell-button" on:click={new_code_cell}>
        <!-- &lt;&sol;&gt; -->
        + Code
    </button>
    <button class="new-cell-button" on:click={new_text_cell}> + Text </button>
</div>

<style>
    .new-cell-toolbar {
        position: absolute;
        bottom: -4px;
        background-color: transparent;
        width: 90%;
        align-content: center;
        justify-content: center;
        height: 6px;
        cursor: default;
        display: flex;
        overflow: hidden;
    }
    .new-cell-toolbar:hover {
        height: 8px;
        background-color: transparent;
        overflow: visible;
    }

    .new-cell-button {
        width: 40px;
        height: fit-content;
        background-color: #ffffff;
        color: #383838;
        cursor: pointer;
        padding: 0%;
        margin: 0px 5px 0px 5px;
        top: -4px;
        position: relative;
        font-size: x-small;
        border-radius: 2px;
        font-family: Verdana, Geneva, Tahoma, sans-serif;
    }
    .new-cell-toolbar .new-cell-button {
        visibility: hidden;
        z-index: -1;
    }
    .new-cell-toolbar:hover .new-cell-button {
        visibility: visible;
        background-color: #cdcdcd;
        z-index: 99;
    }

    /* dark mode */
    @media (prefers-color-scheme: dark) {
        .new-cell-button {
            border: solid 1px #3f3f3f;
            color: #cdcdcd;
        }
        .new-cell-toolbar:hover .new-cell-button {
            background-color: #2b2b2b;
        }
    }
</style>
