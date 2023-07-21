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
    console.log("ycells changed", event, ycells.toJSON());
    cells.set(ycells.toJSON());
});


// NP graph

const ynp_graph = ydoc.getMap('np_graph');
export const np_graph = writable(ynp_graph.toJSON());

ynp_graph.observe((event) => {
    // TODO: optimize this
    console.log("np_graph changed", event, ynp_graph.toJSON());
    np_graph.set(ynp_graph.toJSON());
});

np_graph.subscribe((value) => {
    console.log("np_graph changed", value);
}
);
export const pn_graph = derived(np_graph, $np_graph => {
    // reverse np_graph, which is map of list
    const pn_graph = {};
    for (const prev in $np_graph) {
        for (const next of $np_graph[prev]) {
            if (pn_graph[next] === undefined) {
                pn_graph[next] = [];
            }
            pn_graph[next].push(prev);
        }
    }
    return pn_graph;
}
);
pn_graph.set = (value) => np_graph.update(n => {
    console.error("pn_graph is read-only");
}
);


//  PC graph
const ypc_graph = ydoc.getMap('pc_graph');
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
    // reverse np_graph, which is map of list
    const cp_graph = {};
    for (const parent in $pc_graph) {
        for (const child of $pc_graph[parent]) {
            cp_graph[child] = parent;
        }
    }
    return cp_graph;
}
);
cp_graph.set = (value) => pc_graph.update(n => {
    console.error("cp_graph is read-only");
}
);