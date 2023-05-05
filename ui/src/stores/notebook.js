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
                n.cells[get(id_map)[cell_id]] = cell;
                return n;
            }
            );
        },
        new_code_cell: ({ new_cell, previous_cell_id, id_map, np_graph, pc_graph }) => {
            update(n => {
                // n.cells.splice(previous_cell_index + 1, 0, new_cell);
                n.cells.push(new_cell);

                // update maps
                n["id_map"] = id_map;
                n["np_graph"] = np_graph
                n["pc_graph"] = pc_graph

                console.log(">n:", n);
                return n;
            });
        },
        new_markdown_cell: ({ new_cell, previous_cell_id, id_map, np_graph, pc_graph }) => {
            update(n => {
                const previous_cell = n.cells[id_map[previous_cell_id]];
                const previous_cell_index = n.cells.indexOf(previous_cell);
                // set top, left for new cell
                new_cell["top"] = previous_cell["top"] + previous_cell["height"] + 5;
                new_cell["left"] = previous_cell["left"];
                // insert new cell
                n.cells.splice(previous_cell_index + 1, 0, new_cell);

                // update maps
                n["id_map"] = id_map;
                n["np_graph"] = np_graph
                n["pc_graph"] = pc_graph

                return n;

            });
        },
        clear_outputs: ({ cell_id }) => {
            update(n => {
                const cell = n.cells[get(id_map)[cell_id]];
                if (cell) {
                    cell.outputs = [];
                }
                n.cells[get(id_map)[cell_id]] = cell;
                return n;
            }
            );
        },
        change_cell_state: ({ cell_id, state }) => {
            update(n => {
                n.cells[get(id_map)[cell_id]].state = state;
                return n;
            }
            );
        },
        set_execution_count: ({ cell_id, execution_count }) => {
            update(n => {
                n.cells[get(id_map)[cell_id]].execution_count = execution_count;
                return n;
            }
            );
        },
        resize_ancestors: ({ cell_id }) => {
            // _resize_ancestors(cell_id);
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

// parent-child graph
export const pc_graph = derived(notebook, $notebook => {
    return $notebook.pc_graph
}
);
pc_graph.set = (value) => notebook.update(n => {
    n["pc_graph"] = value;
    return n;
});
//child-parent graph
export const cp_graph = derived(notebook, $notebook => {
    // reverse pc_graph, which is map of list 
    const cp_graph = {};
    // for parent in pc_graph; for child in pc_graph[parent]

    for (const parent in $notebook.pc_graph) {
        for (const child of $notebook.pc_graph[parent]) {
            cp_graph[child] = parent;
        }
    }
    return cp_graph;
}
);
cp_graph.set = (value) => notebook.update(n => {
    console.error("cp_graph is read-only");
});

// next-prev graph
export const np_graph = derived(notebook, $notebook => {
    return $notebook.np_graph
}
);
np_graph.set = (value) => notebook.update(n => {
    n["np_graph"] = value;
    return n;
});
// prev-next graph
export const pn_graph = derived(notebook, $notebook => {
    // reverse np_graph, which is map of list
    const pn_graph = {};
    // for prev in np_graph; for next in np_graph[prev]
    for (const prev in $notebook.np_graph) {
        for (const next of $notebook.np_graph[prev]) {
            if (pn_graph[next] === undefined) {
                pn_graph[next] = [];
            }
            pn_graph[next].push(prev);
        }
    }
    return pn_graph;
}
);
// pn_graph.set = (value) => notebook.update(n => {
//     console.error("pn_graph is read-only");
// });


export function get_heading_level(source) {
    // get markdown heading_level from source
    const heading_level = source[0].match(/#+/g);

    if (heading_level) {
        return heading_level[0].length;
    }
    return null;
}

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

function _find_parent(cell_id) {
    // find parent of cell_id
    let parent_id = null;
    // see in pc_graph if cell_id is a child of any other cell
    Object.entries(get(pc_graph)).forEach(([parent, children]) => {
        if (children.includes(cell_id)) {
            parent_id = parent;
        }
    }
    );
    return parent_id;
}

function _find_ancestors(cell_id) {
    // find ancestors of cell_id
    const ancestors = [];
    let parent_id = _find_parent(cell_id);
    while (parent_id) {
        ancestors.push(parent_id);
        parent_id = _find_parent(parent_id);
    }
    return ancestors;

}

export function _resize_ancestors(cell_id) {
    let ancestors = _find_ancestors(cell_id);
    // for parent in ancestors
    ancestors.forEach(parent_id => {
        let children = get(pc_graph)[parent_id];
        let parent_cell = get(cells)[get(id_map)[parent_id]];

        let x_bounds = [parent_cell.left + parent_cell.width, parent_cell.left];
        let y_bounds = [parent_cell.top + parent_cell.height, parent_cell.top];

        for (let child of children) {
            let child_cell = get(cells)[get(id_map)[child]];
            x_bounds[0] = Math.min(x_bounds[0], child_cell.left);
            x_bounds[1] = Math.max(
                x_bounds[1],
                child_cell.left + child_cell.width
            );
            y_bounds[0] = Math.min(y_bounds[0], child_cell.top);
            y_bounds[1] = Math.max(
                y_bounds[1],
                child_cell.top + child_cell.height
            );
        }
        x_bounds[0] -= 25;
        x_bounds[1] += 25;
        y_bounds[1] += 25;

        // bound
        if (parent_cell.left + parent_cell.width < x_bounds[1]) {
            parent_cell.width = x_bounds[1] - parent_cell.left;
        }
        if (parent_cell.left > x_bounds[0]) {
            parent_cell.left = x_bounds[0];
            parent_cell.width = x_bounds[1] - parent_cell.left;
        }
        if (parent_cell.top + parent_cell.height < y_bounds[1]) {
            parent_cell.height = y_bounds[1] - parent_cell.top;
        }
        if (parent_cell.top > y_bounds[0]) {
            parent_cell.top = y_bounds[0];
            parent_cell.height = y_bounds[1] - parent_cell.top;
        }
        notebook.update(n => {
            n.cells[get(id_map)[parent_id]] = parent_cell;
            return n;
        }
        );

    }
    );
}


export const parent_less_cells = derived([heading_levels, notebook], ([$heading_levels, $notebook]) => {
    const parent_less_cells = [];
    if (!$notebook.cells) {
        return parent_less_cells;
    }
    $notebook.cells.forEach(cell => {
        if (_find_parent(cell.id) === null && !$heading_levels[cell.id]) {
            parent_less_cells.push(cell.id);
        }
    });
    return parent_less_cells;
}
);

import { send_message } from "./socket.js";
export function sync_cell_properties(cell_id) {
    let cell = get(cells)[get(id_map)[cell_id]];
    send_message({
        channel: "notebook",
        method: "sync_cell_properties",
        message: {
            cell_id: cell.id,
            sync: {
                top: cell.top,
                left: cell.left,
                height: cell.height,
                width: cell.width,
            },
        },
    });
}