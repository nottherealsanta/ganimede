import { writable, derived } from 'svelte/store';
import { get } from 'svelte/store'
import * as Y from "yjs";
import { WebsocketProvider } from "y-websocket";
// import { cell_ids as nb_cell_ids, cell_maps } from '../scripts/test_nb';

// Init Yjs

export const ydoc = new Y.Doc();
const websocket_provider = new WebsocketProvider(
    "ws://localhost:1234",
    "g-y-room",
    ydoc
);
websocket_provider.on("status", event => {
    console.log("yjs status: ", event.status); // logs "connected" or "disconnected"
    if (event.status === "disconnected") {
        ydoc.destroy();
        console.log("ydoc destroyed");
        websocket_provider.destroy();
    }

});

// Ycells

export const ycells = ydoc.getArray('cells');
export let cell_ids = ycells.toJSON();
export const is_cell_ids_empty = writable(cell_ids.length === 0);
// export const cells = writable(ycells.toJSON());

ycells.observe((event) => {
    console.log("Ycells event triggered ");
    cell_ids = ycells.toJSON();
    is_cell_ids_empty.set(cell_ids.length === 0);
    update_pc_graph();
});

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
    console.log("pc_graph updated: ", graph);
}

// Command mode
export const is_command_mode = writable(true);

// Active cell
export const active_cell_id = writable("");
export const active_cell_loc = derived(active_cell_id, ($active_cell_id, set) => {
    const cellLoc = cell_ids.indexOf($active_cell_id);
    set(cellLoc);
}
);

// Move Cells
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
}

// Queue Cell 
export function queue_cell(cell_id) {
    fetch(`/queue_cell?cell_id=${cell_id}`)
        .then(response => response.json())
        .then(data => {
            console.log("queue_cell response: ", data);
        });
}