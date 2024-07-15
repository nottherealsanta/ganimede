import { writable, derived } from 'svelte/store';
import { get } from 'svelte/store'
import * as Y from "yjs";
import { WebsocketProvider } from "y-websocket";
import YPartyKitProvider from "y-partykit/provider";
import { send_message } from './comms';

function detectBrowser() {
    var userAgent = navigator.userAgent;
    if (userAgent.indexOf("Edg") > -1) {
        return "Microsoft Edge";
    } else if (userAgent.indexOf("Chrome") > -1) {
        return "Chrome";
    } else if (userAgent.indexOf("Firefox") > -1) {
        return "Firefox";
    } else if (userAgent.indexOf("Safari") > -1) {
        return "Safari";
    } else if (userAgent.indexOf("Opera") > -1) {
        return "Opera";
    } else if (userAgent.indexOf("Trident") > -1 || userAgent.indexOf("MSIE") > -1) {
        return "Internet Explorer";
    }

    return "Unknown";
}



// Init Yjs
export const ydoc = new Y.Doc();

const websocket_provider = new WebsocketProvider(
    "ws://localhost:1234",
    "g-y-room",
    ydoc
);
websocket_provider.on("status", event => {
    console.log("yjs status: ", event.status);
    if (event.status === "disconnected" || event.status === "connecting") {
        ydoc.destroy();
        console.log("ydoc destroyed");
        websocket_provider.destroy();
    }
});


// partykit
// const provider = new YPartyKitProvider(
//     "localhost:1999",
//     "g-y-room-party",
//     ydoc
// );

// Ycells
export const ycells = ydoc.getArray('cells');
export let cell_ids = writable(ycells.toJSON());
export const is_cell_ids_empty = writable(cell_ids.length === 0);

ycells.observe((event) => {
    console.log("Ycells event triggered ");
    // cell_ids = ycells.toJSON();
    cell_ids.set(ycells.toJSON());
    is_cell_ids_empty.set(get(cell_ids).length === 0);
    update_pc_graph();
});

// undo
export const undoManager = new Y.UndoManager(ycells);

// PC Graph
export const pc_graph = writable({});
export function update_pc_graph() {
    const graph = {};
    const parentStack = []; // Stack to keep track of current parents based on heading levels

    ycells.forEach(cell => {
        const cellData = ydoc.getMap(cell).toJSON(); // Assuming cell is a Y.Map and has a toJSON method
        if (cellData.heading_level) {
            // Adjust the stack based on the current heading level
            // Pop from the stack until finding a parent with a lower heading level
            while (parentStack.length > 0 && parentStack[parentStack.length - 1].level >= cellData.heading_level) {
                parentStack.pop();
            }

            // Initialize the children list for the current heading if it doesn't exist
            if (!graph[cellData.id]) {
                graph[cellData.id] = [];
            }

            // If there is a parent, add the current cell as a child to the last parent in the stack
            if (parentStack.length > 0) {
                const currentParentId = parentStack[parentStack.length - 1].id;
                graph[currentParentId].push(cellData.id);
            }

            // Add the current cell as a potential parent for future cells
            parentStack.push({ id: cellData.id, level: cellData.heading_level });
        } else {
            // If it's not a heading, add it to the last heading's children list
            if (parentStack.length > 0) {
                const currentParentId = parentStack[parentStack.length - 1].id;
                if (!graph[currentParentId]) {
                    graph[currentParentId] = [];
                }
                graph[currentParentId].push(cellData.id);
            }
        }
    });
    pc_graph.set(graph);
}

export const cp_graph = derived(pc_graph, $pc_graph => {
    // reverse pc_graph, which is map of list
    const cp_graph = {};
    for (const parent in $pc_graph) {
        for (const child of $pc_graph[parent]) {
            cp_graph[child] = parent;
        }
    }
    return cp_graph;
});
cp_graph.set = (value) => pc_graph.update(n => {
    console.error("cp_graph is read-only");
});

export const n_descendants = derived(pc_graph, $pc_graph => {
    const n_descendants = {};
    const visited = new Set();

    function get_number_of_descendants(cell_id) {
        let count = 0;
        if ($pc_graph[cell_id]) {
            count += $pc_graph[cell_id].length;
            for (let child_id of $pc_graph[cell_id]) {
                count += get_number_of_descendants(child_id);
            }
        }
        return count;
    }

    for (const parent in $pc_graph) {
        visited.clear(); // Clear visited set for each parent
        n_descendants[parent] = get_number_of_descendants(parent);
    }
    return n_descendants;
});

export function propagateCollapse(cell_id, state) {
    // If the cell has children, propagate the state to them
    if (get(pc_graph)[cell_id]) {
        for (let child_id of get(pc_graph)[cell_id]) {
            ydoc.getMap(child_id).set("parent_collapsed", state);
            if (ydoc.getMap(child_id).get('collapsed') != "h") {
                propagateCollapse(child_id, state);
            }
        }
    }
}

// Command mode
export const is_command_mode = writable(true);

// Active cell
export const active_cell_id = writable("");
export const active_cell_loc = derived(active_cell_id, ($active_cell_id, set) => {
    const cellLoc = get(cell_ids).indexOf($active_cell_id);
    set(cellLoc);
}
);

// Move Cells
export const is_dragging = writable(false);

export function drag_move_cells(event) {
    const { oldIndicies, newIndicies, oldIndex, newIndex } = event;
    console.log("drag_move_cells: ", oldIndicies, newIndicies, oldIndex, newIndex);
    // if single cell drag
    if (newIndicies == undefined || newIndicies.length == 0 || newIndicies.length == 1) {
        ycells.doc.transact(() => {
            let currentCells = ycells.toArray();
            const [movedItem] = currentCells.splice(oldIndex, 1);
            currentCells.splice(newIndex, 0, movedItem);
            ycells.delete(0, ycells.length);
            currentCells.forEach((cell) => ycells.push([cell]));
        });
    }
    // multi cells drag 
    else {
        ycells.doc.transact(() => {
            let currentCells = ycells.toArray();
            // Create a copy of oldIndicies and sort it in descending order
            let sortedOldIndicies = [...oldIndicies].sort((a, b) => b.index - a.index);
            let movedItems = [];
            // Remove items from the old positions
            sortedOldIndicies.forEach(oldIndex => {
                const [movedItem] = currentCells.splice(oldIndex.index, 1);
                movedItems.push(movedItem);
            });
            // Reverse the movedItems array
            movedItems.reverse();
            // Insert items at the new positions
            newIndicies.forEach((newIndex, i) => {
                currentCells.splice(newIndex.index, 0, movedItems[i]);
            });
            ycells.delete(0, ycells.length);
            currentCells.forEach((cell) => ycells.push([cell]));
        });
        undoManager.stopCapturing();
    }
    update_pc_graph();

    // if parent is collapsed, expand it
    expand_parent(get(cell_ids)[newIndex]);
}

function expand_parent(cell_id) {
    const parent_id = get(cp_graph)[cell_id];
    if (parent_id) {
        const parent_cell = ydoc.getMap(parent_id).toJSON();
        if (parent_cell.collapsed === "h") {
            ydoc.getMap(parent_id).set("collapsed", "");
            console.log("parent is collapsed, expand it");
            propagateCollapse(parent_id, false);
        }
        if (parent_cell.parent_collapsed) {
            expand_parent(parent_id);
        }
    }
}

// Queue Cell 
export function queue_cell(cell_id) {
    ydoc.getArray('run_queue').push([cell_id]);
}

// Interrupt Cell
export function interrupt(cell_id) {
    ydoc.getArray('run_queue').push(["interrupt"]);
}


// Create Cell
export function create_cell(index, cell_type) {
    console.log("create_cell: ", index, cell_type);
    const cell_id = generateRandomId(8);

    let ycell = ydoc.getMap(cell_id);

    // create cell in ydoc
    ycell.set('id', cell_id);
    ycell.set('type', cell_type);
    ycell.set('source', new Y.Text());
    ycell.set('outputs', new Y.Array());
    ycell.set('execution_count', null);
    ycell.set('heading_level', null);
    ycell.set('collapsed', null);
    ycell.set('parent_collapsed', false);
    ycell.set('state', 'idle');
    ycell.set('execution_time', null);

    ycells.insert(index - 1, [cell_id]);

    active_cell_id.set(cell_id);
    is_command_mode.set(false);

    undoManager.stopCapturing();
}

function generateRandomId(id_length = 8) {
    const n_bytes = Math.max(Math.floor(id_length * 3 / 4), 1);
    const randomBytes = crypto.getRandomValues(new Uint8Array(n_bytes));
    const base64 = btoa(String.fromCharCode.apply(null, randomBytes));
    return base64.slice(0, id_length);
}

// Delete Cell
export function delete_cell(cell_id) {
    console.log("delete_cell: ", cell_id);
    const cell_index = get(cell_ids).indexOf(cell_id);
    ycells.delete(cell_index);
    update_pc_graph();
    undoManager.stopCapturing();

    // active cell
    active_cell_id.set(ycells.get(cell_index));

    is_command_mode.set(true);
}