import { derived, writable } from "svelte/store";
import { get } from 'svelte/store'
import * as Y from "yjs";
import { WebsocketProvider } from "y-websocket";
import { subscribe } from "svelte/internal";

export const html_elements = writable({});
html_elements.set = function (cell_id, element) {
    this[cell_id] = element;
}

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


export const yrun_queue = ydoc.getArray('run_queue');
yrun_queue.observe((event) => {
    // console.log("run_queue: ", event);
});
// ---------- cells
export const ycells = ydoc.getArray('cells');
// export const cells = writable(ycells.toJSON());

ycells.observe((event) => {
});

// ---------- undo
const undoManager = new Y.UndoManager(ycells);

// shortcut
document.addEventListener("keydown", function (event) {
    if ((event.ctrlKey || event.metaKey) && event.key === "z") {
        undoManager.undo();
    }
});

//  ---------- PC graph
export const ypc_graph = ydoc.getMap('pc_graph');
export const pc_graph = writable(new Map());

ypc_graph.observeDeep((event) => {
    // TODO: optimize this
    pc_graph.set(ypc_graph.toJSON());
});



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

// ---------- NP graph

export const ynp_graph = ydoc.getMap('np_graph');
export const np_graph = writable(ynp_graph.toJSON());

ynp_graph.observeDeep((event) => {
    // TODO: optimize this
    // if (!event.transaction.local) {
    np_graph.set(ynp_graph.toJSON());
    // }
});

// np_graph.subscribe((value) => {
//     for (const key in value) {
//         ynp_graph.set(key, value[key]);
//     }
// }
// );

export const pn_graph = derived(np_graph, $np_graph => {
    // reverse np_graph, which is map of list
    const pn_graph = {};
    for (const parent in $np_graph) {
        for (const child of $np_graph[parent]) {
            pn_graph[child] = parent;
        }
    }
    return pn_graph;
});

pn_graph.set = (value) => np_graph.update(n => {
    console.error("pn_graph is read-only");
});

// ---------- New cell

function generateRandomCellId(idLength = 8) {
    const nBytes = Math.max(Math.floor(idLength * 3 / 4), 1);
    const randomBytes = new Uint8Array(nBytes);
    window.crypto.getRandomValues(randomBytes);
    const base64 = btoa(String.fromCharCode.apply(null, randomBytes));
    return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export function create_cell(type, from_cell = null, left = null, top = null) {

    let cell_id = generateRandomCellId();
    let ycell = ydoc.getMap(cell_id);

    // create cell in ydoc
    ycell.set('id', cell_id);
    ycell.set('type', type);
    ycell.set('source', new Y.Text());
    ycell.set('execution_count', null);
    ycell.set('outputs', new Y.Array());
    ycell.set('width', null);
    ycell.set('height', null);
    ycell.set('collapsed', null);
    ycell.set('state', 'idle');


    if (from_cell !== null) {
        let parent = get(cp_graph)[from_cell.id];
        if (parent) {
            // has parent 
            let index = ypc_graph.get(parent).toJSON().indexOf(from_cell.id);
            ypc_graph.get(parent).insert(index + 1, [cell_id]);
            ycell.set('top', null);
            ycell.set('left', null);

        } else {
            // no parent
            ycell.set('top', from_cell.top + from_cell.height + 10);
            ycell.set('left', from_cell.left);
            // set np_graph
            if (!ynp_graph.get(from_cell.id)) {
                let x = new Y.Array();
                x.push([cell_id]);
                ynp_graph.set(from_cell.id, x);
            } else {
                ynp_graph.get(from_cell.id).push([cell_id]);
            }
        }
    } else if (top !== null && left !== null) {
        ycell.set('top', top);
        ycell.set('left', left);
    } else {
        console.error("create_cell: from_cell or top and left must be provided");
    }

    ycells.push([cell_id]);
    undoManager.stopCapturing();
}


// ---------- Delete cell

export function delete_cell(cell_id) {

    console.log("delete cell: ", cell_id);
    // delete from parent's pc_graph
    let parent = get(cp_graph)[cell_id];
    if (parent) {
        // has parent
        let index = ypc_graph.get(parent).toJSON().indexOf(cell_id);
        ypc_graph.get(parent).delete(index, 1);
    }
    // delete from pc_graph
    if (ypc_graph.get(cell_id)) {
        // recusive delete children
        let children = ypc_graph.get(cell_id).toJSON();
        if (children) {
            for (const child of children) {
                delete_cell(child);
            }
        }
        ypc_graph.delete([cell_id]);
    }
    // delete from previous cell's np_graph
    let previous_cell = get(pn_graph)[cell_id];
    if (previous_cell) {
        // has previous cell
        let index = ynp_graph.get(previous_cell).toJSON().indexOf(cell_id);
        ynp_graph.get(previous_cell).delete(index, 1);
    }
    // delete from np_graph
    if (ynp_graph.get(cell_id)) {
        ynp_graph.delete([cell_id]);
    }
    // delete from ycells
    let _index = ycells.toJSON().indexOf(cell_id);
    ycells.delete(_index, 1);
    undoManager.stopCapturing();
}

// ---------- Move cell

export function move_cell(cell_id, dragover_cell, selected_dragzone) {
    // do - dragged over 
    const ycell = ydoc.getMap(cell_id);
    const cell_parent = get(cp_graph)[cell_id];

    // remove from previous parent
    let index_in_parent = null;
    if (cell_parent) {
        const y_cell_parent = ypc_graph.get(cell_parent);
        index_in_parent = y_cell_parent.toJSON().indexOf(cell_id);
        y_cell_parent.delete(index_in_parent, 1);
    }

    function remove_from_np() {
        // prev
        const previous_cell = get(pn_graph)[cell_id];
        if (previous_cell) {
            const y_previous_cell = ynp_graph.get(previous_cell);
            const index = y_previous_cell.toJSON().indexOf(cell_id);
            y_previous_cell.delete(index, 1);
        }
        // next
        if (ynp_graph.get(cell_id)) {
            ynp_graph.delete(cell_id);
        }
    }

    if (dragover_cell) {
        const do_cell_id = dragover_cell.getAttribute('cell_id');
        const do_cell_position = dragover_cell.getAttribute('position');
        const do_parent = get(cp_graph)[do_cell_id];
        if (do_parent) {
            const y_do_parent = ypc_graph.get(do_parent);
            let index = y_do_parent.toJSON().indexOf(do_cell_id);
            if (do_cell_position === 'bottom') {
                index += 1;
            }
            y_do_parent.insert(index, [cell_id]);
            remove_from_np();
        } else {
            // no do_parent
            const do_cell = ydoc.getMap(do_cell_id).toJSON();
            ycell.set('left', do_cell.left);
            if (do_cell_position === 'bottom') {
                ycell.set('top', do_cell.top + do_cell.height + 10);
            } else {
                ycell.set('top', do_cell.top - ycell.get('height') - 10);
            }
        }
    } else if (selected_dragzone) {
        const do_dragzone_id = selected_dragzone.getAttribute('cell_id');

        if (cell_parent !== do_dragzone_id) {
            ypc_graph.get(do_dragzone_id).push([cell_id]);
        } else {
            ypc_graph.get(do_dragzone_id).insert(index_in_parent, [cell_id]);
        }
        remove_from_np();
    }


}