import { derived, writable } from "svelte/store";
import { get } from 'svelte/store';

function createNotebookStore() {
    const { subscribe, set, update } = writable({});

    return {
        subscribe,
        set,
        update,
        append_output: ({ cell_id, output }) => {
            update(n => {
                const cell = n.cells[get(id_map)[cell_id]];
                if (cell) {
                    cell.outputs = [...cell.outputs, output];
                }
                return n;
            }
            );
        },
        new_code_cell: ({ new_cell, previous_cell_id, id_map }) => {
            update(n => {
                const previous_cell = n.cells[id_map[previous_cell_id]];
                const previous_cell_index = n.cells.indexOf(previous_cell);

                // set top, left for new cell
                new_cell["metadata"]["gm"]["top"] = previous_cell["metadata"]["gm"]["top"] + previous_cell["metadata"]["gm"]["height"] + 5;
                new_cell["metadata"]["gm"]["left"] = previous_cell["metadata"]["gm"]["left"];

                // previous's next 
                previous_cell["metadata"]["gm"]["next"] = [...previous_cell["metadata"]["gm"]["next"], new_cell.id];

                // insert new cell
                n.cells.splice(previous_cell_index + 1, 0, new_cell);

                // update id_map
                n["metadata"]["gm"]["id_map"] = id_map;

                return n;
            });
        },
    };
}

export let notebook = createNotebookStore();

export const cells = derived(notebook, $notebook => $notebook.cells);
cells.set = (value) => notebook.update(n => {
    n.cells = value;
    return n;
});

export const id_map = derived(notebook, $notebook => {
    if ($notebook["metadata"] !== undefined) {
        return $notebook["metadata"]["gm"]["id_map"];
    } else {
        return {};
    }
}
);
id_map.set = (value) => notebook.update(n => {
    n["metadata"]["gm"]["id_map"] = value;
    return n;
});
