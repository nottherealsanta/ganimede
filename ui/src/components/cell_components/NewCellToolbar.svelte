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
        $cells[id_map[cell_id]]["metadata"]["gm"]["next"] = [new_cell["id"]];

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
        + Code Cell
    </button>
    <button class="new-cell-button" on:click={new_text_cell}>
        + Text Cell
    </button>
</div>

<style>
    .new-cell-toolbar {
        position: absolute;
        bottom: -4px;
        background-color: transparent;
        width: 90%;
        align-content: center;
        justify-content: center;
        height: 3px;
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
        width: 25%;
        height: fit-content;
        background-color: #ebebeb7d;
        border: solid 1px #c4c4c4;
        color: #5c5c5c;
        cursor: pointer;
        padding: 0%;
        margin: 0px 5px 0px 5px;
        top: -4px;
        position: relative;
        font-size: x-small;
        /* justify-content: center;
        align-content: center; */
    }
    .new-cell-toolbar .new-cell-button {
        visibility: hidden;
    }
    .new-cell-toolbar:hover .new-cell-button {
        visibility: visible;
    }
</style>
