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
                new_cell["top"] = previous_cell["top"] + previous_cell["height"] + 5;
                new_cell["left"] = previous_cell["left"];

                // previous's next 
                previous_cell["next"] = [...previous_cell["next"], new_cell.id];

                // insert new cell
                n.cells.splice(previous_cell_index + 1, 0, new_cell);

                // update id_map
                n["id_map"] = id_map;

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
    return $notebook.id_map
}
);
id_map.set = (value) => notebook.update(n => {
    n["id_map"] = value;
    return n;
});


export function get_heading_level(source) {
    // get markdown heading_level from source
    const heading_level = source[0].match(/#+/g);

    if (heading_level) {
        return heading_level[0].length;
    }
    return null;
}
// create a derived store that returns the heading level of the current cell
// {id: heading_level}
export const heading_levels = derived(notebook, $notebook => {
    const heading_levels = {};
    if (!$notebook.cells) {
        return heading_levels;
    }
    $notebook.cells.forEach(cell => {
        if (cell.type === "markdown") {
            heading_levels[cell.id] = get_heading_level(cell.source);
        }
    });
    return heading_levels;
}
);

export const heading_levels_inv = derived(heading_levels, $heading_levels => {
    const heading_levels_inv = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    };
    Object.entries($heading_levels).forEach(([id, level]) => {
        if (level) {
            heading_levels_inv[level].push(id);
        }
    });
    return heading_levels_inv;
}
);

export const parent_less_cells = derived([heading_levels, notebook], ([$heading_levels, $notebook]) => {
    const parent_less_cells = [];
    if (!$notebook.cells) {
        return parent_less_cells;
    }
    $notebook.cells.forEach(cell => {
        if (cell.parent === null && !$heading_levels[cell.id]) {
            parent_less_cells.push(cell.id);
        }
    });
    return parent_less_cells;
}
);