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



const ycells = ydoc.getArray('cells');
export const cells = writable(ycells.toJSON());

ycells.observe((event) => {
    // TODO: optimize this
    if (!event.transaction.local) {
        cells.set(ycells.toJSON());
    }
});


// cells.subscribe((value) => {
//     // sync ycells with cells
//     for (const key in value) {
//         ycells.insert(parseInt(key), [value[key]]);
//     }
// });

//  PC graph
export const ypc_graph = ydoc.getMap('pc_graph');
export const pc_graph = writable(new Map());

ypc_graph.observe((event) => {
    // TODO: optimize this
    if (!event.transaction.local) {
        pc_graph.set(ypc_graph.toJSON());
    }
});

pc_graph.subscribe((value) => {

    for (const key in value) {
        ypc_graph.set(key, value[key]);
    }
}
);

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

// NP graph

const ynp_graph = ydoc.getMap('np_graph');
export const np_graph = writable(ynp_graph.toJSON());

ynp_graph.observe((event) => {
    // TODO: optimize this
    if (!event.transaction.local) {
        np_graph.set(ynp_graph.toJSON());
    }
});

np_graph.subscribe((value) => {
    for (const key in value) {
        ynp_graph.set(key, value[key]);
    }
}
);

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

// New cell

function generateRandomCellId(idLength = 8) {
    const nBytes = Math.max(Math.floor(idLength * 3 / 4), 1);
    const randomBytes = new Uint8Array(nBytes);
    window.crypto.getRandomValues(randomBytes);
    const base64 = btoa(String.fromCharCode.apply(null, randomBytes));
    return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export function create_cell(type, top, left) {
    let cell_id = generateRandomCellId();
    console.log("create cell", cell_id);
}